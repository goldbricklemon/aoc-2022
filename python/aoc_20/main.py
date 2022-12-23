# -*- coding: utf-8 -*-


class RRItem:

    def __init__(self, number, prev_item=None, next_item=None):
        self.number = number
        self.prev_item = prev_item
        self.next_item = next_item

    def __str__(self):
        return self.number


class RRLinkedList:

    def __init__(self, number_items):
        self.items = number_items
        self.n = len(self.items)
        # self.item_dict = {item.number: item for item in self.items}
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

    def move_number(self, num_item):
        steps = num_item.number
        forward = steps >= 0
        if steps != 0:
            if forward:
                effective_steps = steps % (self.n - 1)
                if effective_steps != 0:
                    insert_at_item = num_item
                    for k in range(effective_steps):
                        insert_at_item = insert_at_item.next_item
                        if k == 0:
                            self.remove(num_item)
                    self.insert(num_item, prev_item=insert_at_item, next_item=insert_at_item.next_item)
            else:
                effective_steps = (-steps) % (self.n - 1)
                if effective_steps != 0:
                    insert_at_item = num_item
                    for k in range(effective_steps):
                        insert_at_item = insert_at_item.prev_item
                        if k == 0:
                            self.remove(num_item)
                    self.insert(num_item, prev_item=insert_at_item.prev_item, next_item=insert_at_item)

    def number_at(self, start_item, pos):
        pos = pos % self.n
        item = start_item
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


def run(numbers, decryption_key=811589153, num_mixes=10):
    numbers = [num * decryption_key for num in numbers]
    number_items = []
    zero_item = None
    for num in numbers:
        item = RRItem(num)
        number_items.append(item)
        if num == 0:
            zero_item = item

    linked_list = RRLinkedList(number_items)
    for i, item in enumerate(linked_list.items):
        print(f"{i}: Prev: {item.prev_item.number}, Num: {item.number}, Next: {item.next_item.number}")

    for _ in range(num_mixes):
        for num_item in number_items:
            linked_list.move_number(num_item)
            # print(linked_list)

    # print(linked_list)
    vals = []
    for pos in [1000, 2000, 3000]:
        vals.append(linked_list.number_at(zero_item, pos=pos))
    print(vals)
    print(sum(vals))


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        numbers = f.readlines()
    numbers = [int(num.strip("\n").strip("\r")) for num in numbers]

    print("#### Star one ####")
    run(numbers, decryption_key=1, num_mixes=1)

    print("#### Star two ####")
    run(numbers)

