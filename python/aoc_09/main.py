# -*- coding: utf-8 -*-
import numpy as np

RIGHT, DOWN, LEFT, UP = "R", "D", "L", "U"
direction_dict = dict(zip([RIGHT, DOWN, LEFT, UP],
                          [np.array([0, 1]),
                           np.array([1, 0]),
                           np.array([0, -1]),
                           np.array([-1, 0])]))


class Knot:

    def __init__(self, name, head=None):
        self.name = name
        self.pos = np.array([0, 0])
        self.tail = None
        if head is not None:
            head.tail = self
        self.coord_store = set()
        self._store_coord()

    def _store_coord(self):
        self.coord_store.add((self.pos[0], self.pos[1]))

    def move_with_vec(self, move_vec: np.ndarray):
        self.pos += move_vec
        # print(f"Knot {self.name} move to {self.pos}")
        self._store_coord()
        if self.tail is not None:
            diff_vec = self.pos - self.tail.pos
            if np.any(np.abs(diff_vec) > 1):
                tail_move_vec = np.sign(diff_vec)
                self.tail.move_with_vec(tail_move_vec)

    def move(self, direction: str, steps: int):
        move_vec = direction_dict[direction]
        for _ in range(steps):
            self.move_with_vec(move_vec)


class Rope:

    def __init__(self, num_knots: int):
        self.knots = []
        for i in range(num_knots):
            head = None if i == 0 else self.knots[i-1]
            knot = Knot(name=i, head=head)
            self.knots.append(knot)

    def move(self, direction, steps):
        self.knots[0].move(direction, steps)


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    direction_steps = list(map(lambda l: (l[0], int(l[2:])), lines))
    print("#### Star one ####")
    rope = Rope(num_knots=2)
    for direction, steps in direction_steps:
        rope.move(direction, steps)
    print(f"Number of tail positions: {len(rope.knots[-1].coord_store)}")

    print("#### Star two ####")
    rope = Rope(num_knots=10)
    for direction, steps in direction_steps:
        rope.move(direction, steps)
    print(f"Number of tail positions: {len(rope.knots[-1].coord_store)}")
