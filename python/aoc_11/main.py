# -*- coding: utf-8 -*-
<<<<<<< HEAD
from functools import reduce


class Op:

    def __init__(self, operation, const_operand=None):
        self.operation = operation
        self.const = const_operand

    def __call__(self, operand):
        o1 = operand
        o2 = operand if self.const is None else self.const
        if self.operation == '+':
            return o1 + o2
        elif self.operation == "*":
            return o1 * o2
        else:
            raise RuntimeError()


class Monkey:

    def __init__(self, monkey_id: int, items: list(), operation: Op, div_test: int, dst_monkey_ids: list(), monkey_broker):
        self.monkey_id = monkey_id
        self.items = items
        self.operation = operation
        self.div_test = div_test
        self.dst_monkey_ids = dst_monkey_ids
        self.monkey_broker = monkey_broker
        self.inspect_count = 0

    def catch_item(self, item):
        self.items.append(item)

    def inspect_items(self, worry_base, save_handling=True):
        for item in self.items:
            self.inspect_count += 1
            item = self.operation(item)
            if save_handling:
                item = item // 3
            else:
                item = item % worry_base
            target_monkey = self.dst_monkey_ids[0] if item % self.div_test == 0 else self.dst_monkey_ids[1]
            self.monkey_broker.throw_item(dst_monkey_id=target_monkey, item=item)
        self.items = []


class MonkeyBroker:

    def __init__(self):
        self.monkeys = dict()
        self.worry_base = 1

    def create_monkey(self, monkey_id: int, items: list(), operation: Op, div_test: int, dst_monkey_ids: list()):
        assert monkey_id not in self.monkeys.keys()
        self.monkeys[monkey_id] = Monkey(monkey_id, items, operation, div_test, dst_monkey_ids, monkey_broker=self)
        self.worry_base = reduce(lambda a, b: a*b, [m.div_test for m in self.monkeys.values()])

    def throw_item(self, dst_monkey_id: int, item: int):
        self.monkeys[dst_monkey_id].catch_item(item)

    def round_of_monkey_business(self, save_handling=True):
        for monkey_id in sorted(self.monkeys.keys()):
            self.monkeys[monkey_id].inspect_items(worry_base=self.worry_base, save_handling=save_handling)

    def get_activity_sorted_monkeys(self):
        return sorted(self.monkeys.values(), key=lambda m: m.inspect_count)


def parse_monkeys(lines):
    mb = MonkeyBroker()
    for l_i in range(0, len(lines), 7):
        monkey_id = int(lines[l_i].lstrip("Monkey ").rstrip(":"))
        items = lines[l_i + 1].lstrip("  Starting items: ").split(", ")
        items = [int(i) for i in items]
        op_string = lines[l_i + 2].lstrip("  Operation: new = old ")
        if op_string.endswith("old"):
            operand = None
        else:
            operand = int(op_string[2:])
        operation = Op(operation=op_string[0], const_operand=operand)
        div_test = int(lines[l_i + 3].lstrip("  Test: divisible by "))
        dst_monkey_ids = [int(lines[l_i + 4].lstrip("    If true: throw to monkey ")),
                          int(lines[l_i + 5].lstrip("    If false: throw to monkey "))]
        mb.create_monkey(monkey_id, items, operation, div_test, dst_monkey_ids)
    return mb
=======
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
>>>>>>> origin/main


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
<<<<<<< HEAD
    mb = parse_monkeys(lines)

    print("#### Star one ####")
    for _ in range(20):
        mb.round_of_monkey_business()

    top_two_monkeys = mb.get_activity_sorted_monkeys()[-2:]
    value = top_two_monkeys[0].inspect_count * top_two_monkeys[1].inspect_count
    print(f"Level of monkey business: {value}")

    print("#### Star two ####")
    mb = parse_monkeys(lines)
    for _ in range(10000):
        mb.round_of_monkey_business(save_handling=False)

    top_two_monkeys = mb.get_activity_sorted_monkeys()[-2:]
    value = top_two_monkeys[0].inspect_count * top_two_monkeys[1].inspect_count
    print(f"Level of monkey business: {value}")
=======
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
>>>>>>> origin/main
