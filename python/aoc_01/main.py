# -*- coding: utf-8 -*-

if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()

    print("#### Star one and two ####")
    lines = [l.strip("\n") for l in lines]
    top_elfs = [0, 0, 0]
    calories = 0

    def insert_calories(new_calories, top_elfs):
        top_elfs = sorted(top_elfs)
        if new_calories > top_elfs[0]:
            top_elfs[0] = new_calories
        return top_elfs

    for line in lines:
        if len(line) > 0:
            calories += int(line)
        else:
            best_three = insert_calories(calories, top_elfs)
            calories = 0
    best_three = insert_calories(calories, top_elfs)
    print(f"Best elf: {max(top_elfs)}")
    print(f"Best three elfs: {top_elfs}, with sum: {sum(top_elfs)}")
