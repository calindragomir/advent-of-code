import sys

from collections import namedtuple
from utils import Utilities

sample = Utilities.get_sample_file(__file__)
real = Utilities.get_full_input(__file__)

titles = {
    # relation-title, table-id
    "seed-to-soil": 1,
    "soil-to-fertilizer": 2,
    "fertilizer-to-water": 3,
    "water-to-light": 4,
    "light-to-temperature": 5,
    "temperature-to-humidity": 6,
    "humidity-to-location": 7,
}

Relation = namedtuple("Relation", "id,source,destination,length")


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def solvep1(lines):
    mappings = build_mappings(lines)
    seeds = [int(i) for i in lines[0].lstrip("seeds: ").split()]
    return solve(mappings, seeds)


def solve_p2_parallel(mappings, seeds_ranges):
    procs = []
    for s, r in pairwise(seeds_ranges):
        procs.append((solve, (mappings, range(s, s+r))))
    locations = Utilities.run_parallel_processes(procs)
    return min(locations)


def solve_p2_single_process(mappings, seeds_ranges):
    locations = []
    for s, r in pairwise(seeds_ranges):
        locations.append(solve(mappings, range(s, s+r)))
    return min(locations)


def solvep2(lines, parallel=False):
    seeds_ranges = [int(i) for i in lines[0].lstrip("seeds: ").split()]
    mappings = build_mappings(lines)
    locations = []
    if parallel:
        return solve_p2_parallel(mappings, seeds_ranges)
    else:
        return solve_p2_single_process(mappings, seeds_ranges)

def solvep2Parallel(lines):
    seeds_ranges = [int(i) for i in lines[0].lstrip("seeds: ").split()]
    mappings = build_mappings(lines)
    procs = []
    for s, r in pairwise(seeds_ranges):
        procs.append((solve, (mappings, range(s, s+r))))
    locations = Utilities.run_parallel_processes(procs)
    return min(locations)


def build_mappings(lines):
    all_relations = []
    current_relation = None
    for index, line in enumerate(lines):
        if line.find("map") != -1:
            title = line.rstrip(" ").rstrip(" map:")
            current_relation = titles[title]
            continue
        if current_relation is not None:
            destination, source, length = (int(i) for i in line.strip().split(" "))
            r = Relation(current_relation, source, destination, length)
            all_relations.append(r)

    mappings = {}
    for r in all_relations:
        content = mappings.get(r.id, [])
        content.append(r)
        mappings[r.id] = content
    return mappings


def solve(mappings, seeds):
    min_location = sys.maxsize
    for seed in seeds:
        checked_id = seed
        for relation_id in titles.values():
            checked_id = get_mapped_id(mappings[relation_id], checked_id)
        if checked_id < min_location:
            min_location = checked_id

    return min_location


def get_mapped_id(relations, checked_id):
    returned_id = checked_id
    for r in relations:
        if r.source <= checked_id <= r.source + r.length - 1:
            offset = checked_id - r.source
            returned_id = r.destination + offset
    return returned_id


if __name__ == '__main__':
    print(solvep1(sample))
    print(solvep2(sample))
    print(solvep1(real))
    print(solvep2(real, parallel=True))
