# -*- coding: utf-8 -*-
import numpy as np


def parse_height_map(lines):
    h, w = len(lines), len(lines[0])
    hmap = np.zeros((h,w), dtype=np.int)
    src, dst = None, None
    for row in range(h):
        for col in range(w):
            c = lines[row][col]
            if c == "S":
                src = (row, col)
                value = ord("a") - 97
            elif c == "E":
                dst = (row, col)
                value = ord("z") - 97
            else:
                value = ord(c) - 97
            hmap[row, col] = value
    return hmap, src, dst


def single_source_shortest_path(hmap: np.ndarray, dst: tuple):
    # Standard Dijkstra's algorithm
    # Real heap is more efficient, but whatever
    queue_costs = []
    queue_items = []
    h, w = hmap.shape

    def valid_index(r, c):
        return (0 <= r < h) and (0 <= c < w)

    cost_map = np.zeros_like(hmap)
    cost_map.fill(h*w + 1)
    cost_map[dst] = 0
    for row in range(h):
        for col in range(w):
            queue_costs.append(cost_map[row, col])
            queue_items.append((row, col))

    pred_map = np.ones((h, w, 2), dtype=np.int) * -1

    while len(queue_items) > 0:
        min_index = np.argmin(queue_costs)
        item, costs = queue_items[min_index], queue_costs[min_index]
        del queue_items[min_index]
        del queue_costs[min_index]
        row, col = item
        height = hmap[row, col]
        for row_offset, col_offset in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            nb_row, nb_col = row + row_offset, col + col_offset
            if valid_index(nb_row, nb_col):
                nb_height = hmap[nb_row, nb_col]
                if height - nb_height <= 1:
                    new_costs = costs + 1
                    if new_costs < cost_map[nb_row, nb_col]:
                        try:
                            queue_index = queue_items.index((nb_row, nb_col))
                            cost_map[nb_row, nb_col] = new_costs
                            queue_costs[queue_index] = new_costs
                            pred_map[nb_row, nb_col] = (row, col)
                        except ValueError:
                            pass

    return cost_map, pred_map


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]

    hmap, src, dst = parse_height_map(lines)
    cost_map, pred_map = single_source_shortest_path(hmap, dst)
    print("#### Star one ####")
    print(f"Steps: {cost_map[src]}")
    print("#### Star two ####")
    starting_locs = np.where(hmap == 0)
    h, w  = hmap.shape
    min_costs = h*w+1
    for row, col in zip(*starting_locs):
        costs = cost_map[row, col]
        min_costs = min(costs, min_costs)
    print(f"Steps: {min_costs}")
