# -*- coding: utf-8 -*-
import numpy as np

AIR, ROCK, SAND = (0, 1, 2)


class Board:

    def __init__(self, rock_paths, min_width=501, source=(0, 500)):
        self.source = source
        max_w, max_h = min_width + 1, 1
        for path in rock_paths:
            for point in path:
                max_h = max(max_h, point[0] + 1)
                max_w = max(max_w, point[1] + 1)

        self.board = np.ones((max_h, max_w), dtype=np.uint8) * AIR
        for path in rock_paths:
            for p1, p2 in zip(path[:-1], path[1:]):
                start = (min(p1[0], p2[0]), min(p1[0], p2[0]))
                end = (max(p1[0], p2[0]), max(p1[0], p2[0]))
                self.board[start[0]:end[0]+1, start[1]:end[1]+1] = ROCK

        self.abyss_y = self.board.shape[0] - 1


if __name__ == '__main__':
    with open("test_input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    paths = [[(int(i) for i in p.split(",")) for p in l.split("->")] for l in lines]
    print("#### Star one ####")

    print("#### Star two ####")
