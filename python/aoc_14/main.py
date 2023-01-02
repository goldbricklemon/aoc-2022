# -*- coding: utf-8 -*-
import numpy as np

AIR, ROCK, SAND = (0, 1, 2)


class Board:

    _mov_vecs = [np.array(a) for a in [[1,0], [1, -1], [1, 1]]]

    def __init__(self, rock_paths, min_width=501, source=[0, 500]):
        self.source = source
        max_w, max_h = min_width + 1, 1
        for path in rock_paths:
            for point in path:
                max_h = max(max_h, point[1] + 1)
                max_w = max(max_w, point[0] + 1)

        self.board = np.ones((max_h, max_w), dtype=np.uint8) * AIR
        for path in rock_paths:
            for p1, p2 in zip(path[:-1], path[1:]):
                start = (min(p1[1], p2[1]), min(p1[0], p2[0]))
                end = (max(p1[1], p2[1]), max(p1[0], p2[0]))
                self.board[start[0]:end[0]+1, start[1]:end[1]+1] = ROCK

        self.abyss_y = self.board.shape[0]
        self.source = np.array(source)

    def run_sand(self):
        abyss_reached = False
        sand_loc = np.copy(self.source)
        while not abyss_reached:
            for mov_vec in self._mov_vecs:
                new_pos = sand_loc + mov_vec
                if new_pos[0] == self.abyss_y:
                    abyss_reached = True
                    break
                elif self.board[tuple(new_pos)] == AIR:
                    sand_loc = new_pos
                    break
            else:
                self.board[tuple(sand_loc)] = SAND
                sand_loc = np.copy(self.source)
                assert self.board[tuple(self.source)] != SAND

    def num_sand(self):
        return np.sum(np.equal(self.board, SAND))


if __name__ == '__main__':
    with open("test_input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    paths = [[tuple(int(i) for i in p.split(",")) for p in l.split("->")] for l in lines]
    board = Board(rock_paths=paths)
    board.run_sand()
    print("#### Star one ####")
    print(f"NUM SAND: {board.num_sand()}")
    print("#### Star two ####")
