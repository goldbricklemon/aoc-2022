# -*- coding: utf-8 -*-
"""
Created on 21 Dec 2022, 09:55

@author: einfalmo
"""
import copy


class RRItem:

    def __init__(self, number, prev_item=None, next_item=None):
        self.number = number
        self.prev_item = prev_item
        self.next_item = next_item

    def __str__(self):
        return self.number


class RRLinkedList:

    def __init__(self, numbers):
        self.items = [RRItem(num) for num in numbers]
        self.n = len(self.items)
        self.item_dict = {item.number: item for item in self.items}
        for i in range(self.n):
            prev_i = (i - 1) % self.n
            next_i = (i + 1) % self.n
            prev_item, item, next_item = [self.items[i] for i in [prev_i, i, next_i]]
            self.link(prev_item, item)
            self.link(item, next_item)

    def link(self, prev_item, next_item):
        prev_item.next_item = next_item
        next_item.prev_item = prev_item

    def unlink(self, prev_item, next_item):
        prev_item.next_item = None
        next_item.prev_item = None

    def remove(self, item):
        prev_item, next_item = item.prev_item, item.next_item
        self.unlink(item.prev_item, item)
        self.unlink(item, item.next_item)
        self.link(prev_item, next_item)

    def insert(self, item, prev_item, next_item):
        self.link(prev_item, item)
        self.link(item, next_item)

    def move_number(self, num):
        item = self.item_dict[num]
        steps = num
        forward = steps >= 0
        if steps != 0:
            if forward:
                effective_steps = steps % (self.n - 1)
                if effective_steps != 0:
                    insert_at_item = item
                    for k in range(effective_steps):
                        insert_at_item = insert_at_item.next_item
                        if k == 0:
                            self.remove(item)
                    self.insert(item, prev_item=insert_at_item, next_item=insert_at_item.next_item)
            else:
                effective_steps = (-steps) % (self.n - 1)
                if effective_steps != 0:
                    insert_at_item = item
                    for k in range(effective_steps):
                        insert_at_item = insert_at_item.prev_item
                        if k == 0:
                            self.remove(item)
                    self.insert(item, prev_item=insert_at_item.prev_item, next_item=insert_at_item)

    def number_at(self, start_num, pos):
        pos = pos % self.n
        item = self.item_dict[start_num]
        for k in range(pos):
            item = item.next_item
        return item.number

    def __str__(self):
        item = self.items[0]
        s = str(item.number)
        for i in range(self.n - 1):
            item = item.next_item
            s += f", {item.number}"
        return s


if __name__ == '__main__':
    with open("test_input.txt", "r") as f:
        numbers = f.readlines()
    numbers = [int(num.strip("\n")) for num in numbers]

    linked_list = RRLinkedList(copy.copy(numbers))
    for i, item in enumerate(linked_list.items):
        print(f"{i}: Prev: {item.prev_item.number}, Num: {item.number}, Next: {item.next_item.number}")

    for num in numbers:
        linked_list.move_number(num)
        # print(linked_list)

    # print(linked_list)
    vals = []
    for pos in [1000, 2000, 3000]:
        vals.append(linked_list.number_at(0, pos=pos))
    print(vals)
    print(sum(vals))
