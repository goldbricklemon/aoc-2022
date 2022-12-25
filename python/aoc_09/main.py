# -*- coding: utf-8 -*-
import numpy as np
from functools import reduce

RIGHT, DOWN, LEFT, UP = "R", "D", "L", "U"
direction_dict = dict(zip([RIGHT, DOWN, LEFT, UP],
                          [np.array([0, 1]),
                           np.array([1, 0]),
                           np.array([0, -1]),
                           np.array([-1, 0])]))


class Rope:

    def __init__(self):
        self.head = np.array([0, 0])
        self.tail = np.copy(self.head)
        self.tail_coord_store = set()
        self._store_coord(self.tail)

    def _store_coord(self, coord: np.ndarray):
        self.tail_coord_store.add((coord[0], coord[1]))

    def move_head(self, direction: str, steps: int):
        move_vec = direction_dict[direction]
        for _ in range(steps):
            self.head += move_vec
            diff_vec = self.head - self.tail
            if np.any(np.abs(diff_vec) > 1):
                tail_move_vec = np.sign(diff_vec)
                self.tail += tail_move_vec
                self._store_coord(self.tail)


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    direction_steps = map(lambda l: (l[0], int(l[2:])), lines)
    print("#### Star one ####")
    rope = Rope()
    for direction, steps in direction_steps:
        rope.move_head(direction, steps)
    print(f"Number of tail positions: {len(rope.tail_coord_store)}")

    print("#### Star two ####")
