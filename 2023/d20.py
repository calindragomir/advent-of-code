from collections import deque
from itertools import count
from math import lcm

import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

FF = "%"
CJ = "&"
BROADCASTER = "broadcaster"
BUTTON = "button"
PRESSES = 1000

flip_flops = {}
conjunctions = {}
graph = {}


def find_periods(graph, flipflops, conjunctions):
    periodic = set()

    for rx_source, dests in graph.items():
        if dests == ['rx']:
            break

    for source, dests in graph.items():
        if rx_source in dests:
            periodic.add(source)

    for iteration in count(1):
        q = deque([(BUTTON, BROADCASTER, False)])

        while q:
            sender, receiver, pulse = q.popleft()

            if not pulse:
                if receiver in periodic:
                    yield iteration

                    periodic.discard(receiver)
                    if not periodic:
                        return

            q.extend(process_pulse(graph, flipflops, conjunctions, sender, receiver, pulse))


def process_pulse(graph, flipflops, conjunctions, sender, receiver, pulse):
    if receiver in flipflops:
        if pulse:
            return
        next_pulse = flipflops[receiver] = not flipflops[receiver]
    elif receiver in conjunctions:
        conjunctions[receiver][sender] = pulse
        next_pulse = not all(conjunctions[receiver].values())
    elif receiver in graph:
        next_pulse = pulse
    else:
        return

    for new_receiver in graph[receiver]:
        yield receiver, new_receiver, next_pulse


def run(graph, flops, conjs):
    q = deque([('button', BROADCASTER, False)])
    number_highs = number_lows = 0

    while q:
        sender, receiver, pulse = q.popleft()
        number_highs += pulse
        number_lows += not pulse
        q.extend(process_pulse(graph, flops, conjs, sender, receiver, pulse))

    return number_highs, number_lows


def solve(lines, part2=False):
    for line in lines:
        source, destinations = line.split("->")
        source = source.strip()
        destinations = destinations.strip().split(", ")

        if source[0] == FF:
            source = source[1:]
            flip_flops[source] = False
        elif source[0] == CJ:
            source = source[1:]
            conjunctions[source] = {}

        graph[source] = destinations

    for source, destinations in graph.items():
        for dest in filter(conjunctions.__contains__, destinations):
            conjunctions[dest][source] = False

    if not part2:
        total_highs = total_lows = 0
        for _ in range(PRESSES):
            number_highs, number_lows = run(graph, flip_flops, conjunctions)
            total_highs += number_highs
            total_lows += number_lows

        return total_lows * total_highs

    for f in flip_flops:
        flip_flops[f] = False

    for inputs in conjunctions.values():
        for i in inputs:
            inputs[i] = False

    return lcm(*find_periods(graph, flip_flops, conjunctions))


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(sample, True))
    print(solve(full, True))
