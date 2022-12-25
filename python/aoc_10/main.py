# -*- coding: utf-8 -*-
import numpy as np


class Instruction:

    opcode = None
    total_cycles = 1

    def __init__(self):
        self.cycles = 0

    def run_cycle(self, registers: dict):
        assert self.cycles < self.total_cycles
        self.cycles += 1

        if self.cycles == self.total_cycles:
            return True, registers
        else:
            return False, registers


class NoOp(Instruction):

    opcode = "noop"
    total_cycles = 1


class AddOp(Instruction):

    opcode = "add"
    total_cycles = 2

    def __init__(self, operand, accum_register="x"):
        super(AddOp, self).__init__()
        self.accum_register = accum_register
        self.operand = operand

    def run_cycle(self, registers: dict):
        assert self.cycles < self.total_cycles
        self.cycles += 1

        if self.cycles == self.total_cycles:
            tmp = registers[self.accum_register]
            registers[self.accum_register] = tmp + self.operand
            return True, registers
        else:
            return False, registers


class CPU:

    instruction_set = {optype: optype.opcode for optype in [NoOp, AddOp]}

    def __init__(self, instructions, register_names):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.registers = {r: 1 for r in register_names}

    def run_cycle(self):
        if self.instruction_pointer < len(self.instructions):
            op = self.instructions[self.instruction_pointer]
        else:
            op = NoOp()
        op_done, self.registers = op.run_cycle(registers=self.registers)
        if op_done:
            self.instruction_pointer += 1


class SpriteCRT:

    def __init__(self, height, width, cpu_registers):
        self.height = height
        self.width = width
        self.cpu_registers = cpu_registers
        self.row = 0
        self.col = 0
        self.draw_buffer = ""

    def draw_pixel(self):

        # Do drawing
        sprite_pos = self.cpu_registers["x"]
        pix = '.'
        if self.col in range(sprite_pos - 1, sprite_pos + 2):
            pix = "#"
        self.draw_buffer += pix

        self.col += 1
        if self.col == self.width:
            self.col = 0
            self.row += 1
            self.draw_buffer += "\n"
            if self.row == self.height:
                self.row = 0
                print(self.draw_buffer)
                self.draw_buffer = ""


def parse_instructions(lines):
    instructions = []
    for line in lines:
        if line.startswith("noop"):
            op = NoOp()
        else:
            operand = int(line[5:])
            op = AddOp(operand=operand, accum_register="x")

        instructions.append(op)
    return instructions


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    instructions = parse_instructions(lines)
    cpu = CPU(instructions, register_names=["x"])
    crt = SpriteCRT(height=6, width=40, cpu_registers=cpu.registers)
    print("#### Star one and two ####")
    print("")
    max_cycles = 240
    register_history = []
    history_cycles = [20, 60, 100, 140, 180, 220]
    for cycle in range(1, max_cycles + 1):
        if cycle in history_cycles:
            register_history.append(cpu.registers["x"])
        crt.draw_pixel()
        cpu.run_cycle()

    signal_strength = np.sum(np.array(history_cycles) * np.array(register_history))
    print(f"Signal Strength {signal_strength}")
