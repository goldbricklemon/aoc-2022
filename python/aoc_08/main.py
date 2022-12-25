# -*- coding: utf-8 -*-
import numpy as np
from functools import reduce


def read_input(lines):
    tree_rows = list(map(lambda l: np.array([int(c) for c in l]), lines))
    return np.stack(tree_rows, axis=0)

def visible_tree_map_and_scenic_scores(trees):
    # Let's be efficient and cache the ten tree height occupancy maps
    occupancy_maps = [trees >= i for i in range(10)]
    visible_map = np.ones(shape=trees.shape, dtype=np.bool)
    h, w = trees.shape
    scenic_scores = np.zeros((h, w, 4), dtype=np.int)

    for row in range(0, h):
        for col in range(0, w):
            tree_height = trees[row, col]
            occupancy_map = occupancy_maps[tree_height]
            sight_lines = [occupancy_map[row, 0:col][::-1],
                                occupancy_map[row, col+1:],
                                occupancy_map[0:row, col][::-1],
                                occupancy_map[row+1:, col]
                                ]
            visible = any([not np.any(sight_blocked) for sight_blocked in sight_lines])
            visible_map[row, col] = visible

            for l_i, sight_blocked in enumerate(sight_lines):
                for blocked in sight_blocked:
                    scenic_scores[row, col, l_i] += 1
                    if blocked:
                        break
    # Multiply the four direction scenic scores
    scenic_scores = reduce(lambda a, b: a * b, [scenic_scores[..., i] for i in range(4)])
    return visible_map, scenic_scores


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]

    trees = read_input(lines)
    print("#### Star one ####")
    visible_map, scenic_scores = visible_tree_map_and_scenic_scores(trees)
    print(f"Visible trees: {np.sum(visible_map)}")

    print("#### Star two ####")
    print(f"Max. scenic score: {np.max(scenic_scores)}")
