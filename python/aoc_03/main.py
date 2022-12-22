# -*- coding: utf-8 -*-

def char_to_priority(character):
    if character.isupper():
        return ord(character) - 65 + 27
    else:
        return ord(character) - 97 + 1


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n") for l in lines]

    print("#### Star one ####")
    score = 0
    for line in lines:
        a, b = line[:len(line)//2], line[len(line)//2:]
        found = None
        for charater in a:
            if charater in b:
                found = charater
                break
        score += char_to_priority(found)
    print(f"Score: {score}")

    print("#### Star two ####")
    score = 0
    groups = zip(lines[::3], lines[1::3], lines[2::3])
    for group in groups:
        a, b, c = group
        found = None
        for charater in a:
            if charater in b and charater in c:
                found = charater
                break
        score += char_to_priority(found)
    print(f"Score: {score}")
