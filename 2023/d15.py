import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

boxes = {i: {} for i in range(256)}


def handle_equal(i):
    label, focal_length = i.split("=")
    box_id = run_the_hash_algo(label)
    boxes[box_id][label] = int(focal_length)


def handle_minus(label):
    box_id = run_the_hash_algo(label)
    if label in boxes[box_id]:
        del boxes[box_id][label]


def calculate_focusing():
    focusing_powers = []
    for box_id, lenses in boxes.items():
        for idx, lens in enumerate(lenses):
            focusing_powers.append((box_id+1) * (idx+1) * lenses[lens])
    return sum(focusing_powers)


def solve(lines, part2=False):
    hash_values = []
    if not part2:
        for line in lines:
            inputs = line.split(",")
            for i in inputs:
                hash_values.append(run_the_hash_algo(i))

        return sum(hash_values)

    for line in lines:
        inputs = line.split(",")
        for i in inputs:
            if i[-2] == "=":
                handle_equal(i)
            elif i[-1] == "-":
                handle_minus(i[:-1])

    return calculate_focusing()


def run_the_hash_algo(part):
    output = 0
    for c in part:
        output = (output + ord(c)) * 17 % 256
    return output


if __name__ == '__main__':
    #print(solve(sample))
    #print(solve(sample, True))
    print(solve(full))
    print(solve(full, True))

