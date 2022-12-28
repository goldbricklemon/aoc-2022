# -*- coding: utf-8 -*-
import json
import itertools
import functools


class Packet:

    def __init__(self, content):
        self.content = content


def sanitize_items(i1, i2):
    if type(i1) is list and type(i2) is int:
        return i1, [i2]
    elif type(i2) is list and type(i1) is int:
        return [i1], i2
    else:
        return i1, i2


def cmp_packets(p1, p2):
    p1, p2 = sanitize_items(p1, p2)
    if type(p1) is int:
        if p1 < p2:
            return -1
        elif p1 > p2:
            return 1
    else:
        for i1, i2 in zip(p1, p2):
            ret = cmp_packets(i1, i2)
            if ret is not None:
                return ret
        if len(p1) < len(p2):
            return -1
        elif len(p1) > len(p2):
            return 1
    return None


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    packet_pairs = [(Packet(json.loads(l1)), Packet(json.loads(l2))) for l1, l2 in zip(lines[::3], lines[1::3])]

    print("#### Star one ####")
    correct = 0
    for i, (p1, p2) in enumerate(packet_pairs):
        ret = cmp_packets(p1.content, p2.content)
        if ret == -1:
            correct += i + 1
    print(f"Correct: {correct}")

    print("#### Star two ####")
    divider_packets = [Packet([[2]]),
                       Packet([[6]])]
    packets = list(itertools.chain(*packet_pairs)) + divider_packets
    packets = sorted(packets, key=functools.cmp_to_key(lambda p1, p2: cmp_packets(p1.content, p2.content)))
    key = functools.reduce(lambda a, b: a * b, [packets.index(p) + 1 for p in divider_packets])
    print(f"Decode key: {key}")
