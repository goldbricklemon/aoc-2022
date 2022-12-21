# -*- coding: utf-8 -*-

if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()

    print("#### Star one and two ####")
    lines = [l.strip("\n") for l in lines]
    best_three = [0, 0, 0]
    calories = 0

    def insert_calories(new_calories, best_three):
        best_three = sorted(best_three)
        if new_calories > best_three[0]:
            best_three[0] = new_calories
        return best_three

    for line in lines:
        if len(line) > 0:
            calories += int(line)
        else:
            best_three = insert_calories(calories, best_three)
            calories = 0
    best_three = insert_calories(calories, best_three)
    print(f"Best elf: {max(best_three)}")
    print(f"Best three elfs: {best_three}, with sum: {sum(best_three)}")
