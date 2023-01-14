# -*- coding: utf-8 -*-
import re

digit_re = re.compile(r"-?\d+")


class Sensor:

    def __init__(self, x, y, beacon_x, beacon_y):
        self.x = int(x)
        self.y = int(y)
        self.beacon_x = int(beacon_x)
        self.beacon_y = int(beacon_y)
        self.r = abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)

    # def __str__(self):
    #     msg = f"Sensor at ({self.x}, {self.y}) with Beacon at ({self.beacon_x}, {self.beacon_y}) hat coverage r={self.r}"
    #     return msg

    def coverage_range_at_row(self, row):
        ydist = abs(self.y - row)
        range = None
        if ydist <= self.r:
            range = [self.x - self.r + ydist, self.x + self.r - ydist]
            if self.beacon_y == row:
                ranges = [[range[0], self.beacon_x - 1], [self.beacon_x + 1, range[1]]]
                ranges = [r for r in ranges if r[1] >= r[0]]
                range = ranges[0] if len(ranges) == 1 else None
        return range


def merge_range(r1, r2):
    if r2[0] > r1[1]:
        return False, r1
    else:
        return True, [r1[0], max(r1[1], r2[1])]


def merge_all_ranges(ranges):
    merged_ranges = []
    ranges = sorted(ranges)
    r1 = ranges[0]
    for r2 in ranges[1:]:
        can_merge, r1 = merge_range(r1, r2)
        if not can_merge:
            merged_ranges.append(r1)
            r1 = r2
    merged_ranges.append(r1)
    return merged_ranges


if __name__ == '__main__':
    input_file = "input.txt"
    row = 10 if "test" in input_file else 2000000
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    sensors = [Sensor(*digit_re.findall(l)) for l in lines]
    print("#### Star one ####")
    all_ranges = [r for r in map(lambda s: s.coverage_range_at_row(row), sensors) if r is not None]
    merged = merge_all_ranges(all_ranges)
    covered = sum([r[1] - r[0] + 1 for r in merged])
    print(f"Covered: {covered}")
    print("#### Star two ####")
