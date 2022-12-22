# -*- coding: utf-8 -*-


def parse_ranges(line):
    r1, r2 = line.split(",")
    r1, r2 = [r.split("-") for r in [r1, r2]]
    r1, r2 = [(int(r[0]), int(r[1])) for r in [r1, r2]]
    return r1, r2


def contains_range(r1, r2):
    return r1[0] <= r2[0] and r1[1] >= r2[1]


def ranges_overlap(r1, r2):
    return r1[0] <= r2[0] <= r1[1] or r1[0] <= r2[1] <= r1[1]


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    range_pairs = [parse_ranges(l) for l in lines]

    print("#### Star one ####")
    full_overlap_pairs = 0
    any_overlap_pairs = 0
    for r1, r2 in range_pairs:
        full_overlap_pairs += int(contains_range(r1, r2) or contains_range(r2, r1))
        any_overlap_pairs += int(ranges_overlap(r1, r2) or ranges_overlap(r2, r1))

    print(f"Full overlap elf pairs: {full_overlap_pairs}")

    print("#### Star two ####")
    print(f"Any overlap elf pairs: {any_overlap_pairs}")
