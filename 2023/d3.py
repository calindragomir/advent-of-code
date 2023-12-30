from utils import Utilities
from ordered_set import OrderedSet

sample = Utilities.get_lines_from_file("sample/d3p1sample.txt")
sample2 = Utilities.get_lines_from_file("sample/d3p1sample2.txt")
sample3 = Utilities.get_lines_from_file("sample/d3p1sample3.txt")
full_input = Utilities.get_lines_from_file("d3.txt")

markings = ["SYMBOL", "NONE"]

def solve(lines):
    number_indexes = []  # all locations where there is a number
    symbol_indexes = {}  # locations of symbols
    all_numbers = []
    for index, line in enumerate(lines):
        line_indexes = []
        num = 0
        line_length = len(line)
        for index_detail, detail in enumerate(line):
            if detail.isdigit():  # we encountered a number, start storing the digits
                num = num * 10 + int(detail)
                line_indexes.append((index, index_detail))
            if not detail.isdigit():  # this means num is completed, can save the index and reset number
                if num > 0:
                    number_indexes.append((num, line_indexes))
                    all_numbers.append(num)
                    num = 0
                    line_indexes = []
            if index_detail + 2 > line_length:  # make sure to include last number
                if num > 0:
                    number_indexes.append((num, line_indexes))
                    all_numbers.append(num)
            handle_symbol(index, index_detail, detail, symbol_indexes)

    parts_locations = get_parts_locations(symbol_indexes)
    parts_numbers = get_parts_numbers(parts_locations, number_indexes)
    gear_ratios = calculate_gear_ratios(symbol_indexes, number_indexes)

    return sum(parts_numbers), sum(gear_ratios)


def get_parts_numbers(parts_locations, number_indexes):
    parts = []
    for number_info in number_indexes:
        if check_number(number_info[1], parts_locations):
            parts.append(number_info[0])

    return parts


def check_number(num_locations, parts_locations):
    for location in num_locations:
        if location in parts_locations:
            return True

    return False

def get_parts_locations(symbol_indexes):
    parts_locations = set()
    for symbol_sets in symbol_indexes.values():
        for symbol_location in symbol_sets:
            for n in range(3):
                parts_locations.add((symbol_location[0] - 1, symbol_location[1] - 1 + n))
            for n in range(3):
                parts_locations.add((symbol_location[0] + 1, symbol_location[1] - 1 + n))
            parts_locations.add((symbol_location[0], symbol_location[1] - 1))
            parts_locations.add((symbol_location[0], symbol_location[1] + 1))
    return parts_locations


def calculate_gear_ratios(symbol_indexes, number_indexes):
    gear_ratio_nums = []
    for symbol_value, symbol_sets in symbol_indexes.items():
        if symbol_value != "*":
            continue

        for symbol_location in symbol_sets:
            gears_locations = set()
            for n in range(3):
                gears_locations.add((symbol_location[0] - 1, symbol_location[1] - 1 + n))
            for n in range(3):
                gears_locations.add((symbol_location[0] + 1, symbol_location[1] - 1 + n))
            gears_locations.add((symbol_location[0], symbol_location[1] - 1))
            gears_locations.add((symbol_location[0], symbol_location[1] + 1))

            adj_num = []
            for num in number_indexes:
                a = num[0]
                b = num[1]
                for i in b:
                    if i in gears_locations:
                        adj_num.append(a)
                        break

            if len(adj_num) == 2:
                gear_ratio_nums.append(adj_num[0] * adj_num[1])

    return gear_ratio_nums


def handle_symbol(index, index_detail, detail, symbol_indexes):
    if not detail.isdigit() and detail != ".":
        if detail in symbol_indexes.keys():
            symbol_indexes[detail].add((index, index_detail))
        else:
            symbol_indexes[detail] = OrderedSet([(index, index_detail)])


if __name__ == '__main__':
    print(solve(sample))
    print(solve(sample2))
    print(solve(sample3))
    print(solve(full_input))

