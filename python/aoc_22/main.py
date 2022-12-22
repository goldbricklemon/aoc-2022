# -*- coding: utf-8 -*-

import copy
import numpy as np

PORTAL, FREE, WALL = 0, 1, 2
character_mapping = dict(zip([" ", ".", "#"], [PORTAL, FREE, WALL]))

DIRECTIONS = range(4)
RIGHT, DOWN, LEFT, UP = DIRECTIONS
MOVE_VECS = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])]

# Small hack to differentiate turn from move operations
TURN_LEFT, TURN_RIGHT = -3, -1


def next_direction(current_dir: int, turn_op: int):
    return DIRECTIONS[(current_dir + turn_op + 2) % 4]


def parse_instructions(instructions: str):
    # Note: This assumes instructions in a fixed [turn, move, turn, move, ...] order
    # This code breaks otherwise
    instructions = instructions.replace("R", f",{TURN_RIGHT},")
    instructions = instructions.replace("L", f",{TURN_LEFT},")
    instructions.lstrip(",").rstrip(",")
    instruction_ops = instructions.split(",")
    instruction_ops = [int(op) for op in instruction_ops]
    return instruction_ops


class Board:

    @classmethod
    def create_from_lines(cls, lines: list):
        board_width = max([len(l) for l in lines])
        board_height = len(lines)

        board_input = np.zeros((board_height, board_width), dtype=np.int)
        board_input[:, :] = PORTAL
        for y, line in enumerate(lines):
            for x, character in enumerate(line):
                board_input[y, x] = character_mapping[character]

        return Board(board_input)

    def __init__(self, board_input: np.ndarray):
        self.board = board_input
        # We pad the board with one tile of PORTAL to avoid any OOB checks
        self.board = np.pad(self.board, ((1, 1), (1, 1)), mode="constant", constant_values=PORTAL)
        self.h, self.w = self.board.shape
        self.position = np.array([1, 0], dtype=np.int)
        self.position[1] = np.where(np.equal(self.board[1], FREE))[0][0]
        self.direction = RIGHT

    def get_board_value(self, position):
        return self.board[position[0], position[1]]

    def get_player_state(self):
        # Do not adjust for border, since final answer requires 1-index position
        return self.position[0], self.position[1], self.direction

    def do_operation(self, op):
        if op < 0:
            # TURN op
            self.direction = next_direction(self.direction, op)
            # print(f"Turn to {self.direction}")
        else:
            # MOVE op
            move_vec = MOVE_VECS[self.direction]
            for _ in range(op):
                new_pos = self.position + move_vec
                board_value = self.get_board_value(new_pos)
                if board_value == FREE:
                    self.position = new_pos
                    # print(f"Move to {self.position}")
                elif board_value == WALL:
                    break
                else:
                    scan_position, value = self._scan_from_portal(new_pos, move_vec)
                    if value == FREE:
                        self.position = scan_position
                        # print(f"Portal to {self.position}")
                    else:
                        break

    def _scan_from_portal(self, portal_position, move_vec):
        scan_position = np.copy(portal_position)
        if self.direction == RIGHT:
            scan_position[1] = 0
        elif self.direction == DOWN:
            scan_position[0] = 0
        elif self.direction == LEFT:
            scan_position[1] = self.w - 1
        else:
            scan_position[0] = self.h - 1

        while True:
            value = self.get_board_value(scan_position)
            if value in [FREE, WALL]:
                return scan_position, value
            else:
                scan_position += move_vec


def parse_lines(lines: list):
    instruction_ops = parse_instructions(lines[-1])
    lines = lines[:-2]
    board = Board.create_from_lines(lines)
    return board, instruction_ops


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]

    print("#### Star one ####")
    board, instructions = parse_lines(lines)
    for op in instructions:
        board.do_operation(op)

    y, x, dir = board.get_player_state()
    print(f"Y: {y}, X: {x}, DIR: {dir}")
    passwd = y * 1000 + x * 4 + dir
    print(f"Password: {passwd}")

