# -*- coding: utf-8 -*-

def insert_calories(calories, top_elfs):
    top_elfs = sorted(top_elfs)
    if calories > top_elfs[0]:
        top_elfs[0] = calories
    return top_elfs


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()

    print("#### Star one and two ####")
    lines = [l.strip("\n").strip("\r") for l in lines]
    top_elfs = [0, 0, 0]
    calories = 0

    for line in lines:
        if len(line) > 0:
            calories += int(line)
        else:
            top_elfs = insert_calories(calories, top_elfs)
            calories = 0
    top_elfs = insert_calories(calories, top_elfs)
    print(f"Best elf: {max(top_elfs)}")
    print(f"Best three elfs: {top_elfs}, with sum: {sum(top_elfs)}")
