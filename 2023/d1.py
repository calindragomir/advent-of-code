from utils import Utilities

lines = Utilities.get_full_input(__file__)
linesSample = Utilities.get_lines_from_file("sample/d1p1sample.txt")
linesSampleLetters = Utilities.get_lines_from_file("sample/d1p2sample.txt")
linesCustom = Utilities.get_lines_from_file("sample/d1customsample.txt")
letter_numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def calculate_sum(lines):
    total = 0
    for line in lines:
        n = [i for i in line if i.isdigit()]
        if len(n) == 0:
            continue
        if len(n) == 1:
            doublenum = n[0]*2
            total += int(doublenum)
        if len(n) > 1:
            number = n[0] + n[-1]
            total += int(number)

    return total


def calculate_letters(lines):
    total = 0
    for line in lines:
        num = 0
        letter_indexes = get_indexes_for_letters(line)
        digits_indexes = get_indexes_for_digits(line)
        indexes = letter_indexes + digits_indexes
        indexes.sort(key=lambda x: x[0])
        if len(indexes) == 0:
            continue
        if len(indexes) == 1:
            num = indexes[0][1] * 10 + indexes[0][1]
        if len(indexes) > 1:
            num = indexes[0][1] * 10 + indexes[-1][1]

        #print("%s : %s" % (line, num))
        total += num

    return total


def get_indexes_for_letters(line):
    indexes = []
    for letternumb in letter_numbers.keys():
        searchline = line
        offset = 0
        while len(searchline) > 0:
            i = searchline.find(letternumb)
            if i > -1:
                indexes.append((i+offset, letter_numbers[letternumb]))
                searchline = searchline[i+1:]
                offset += i + 1
            else:
                break

    return indexes


def get_indexes_for_digits(line):
    indexes = []
    for i, letter in enumerate(line):
        if letter.isdigit():
            indexes.append((i, int(letter)))

    return indexes


if __name__ == '__main__':
    print("example: %s" % calculate_sum(linesSample))
    print("part1: %s" % calculate_sum(lines))
    print("part2: %s" % calculate_letters(lines))