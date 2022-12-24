# -*- coding: utf-8 -*-
import numpy as np


class FileSystemObject:

    def __init__(self, name: str, parent_dir):
        self.name = name
        self.parent_dir = parent_dir

    def get_size(self):
        return 0


class File(FileSystemObject):

    def __init__(self, name:str, parent_dir: FileSystemObject, size: int):
        super().__init__(name, parent_dir)
        self.size = size

    def get_size(self):
        return self.size


class Directory(FileSystemObject):

    def __init__(self, name: str, parent_dir: FileSystemObject, content=[]):
        super().__init__(name, parent_dir)
        self.content = [c for c in content]

    def get_size(self):
        return sum([file.get_size() for file in self.content])

    def add_file_system_object(self, fso: FileSystemObject):
        # Only add if not existing
        t = type(fso)
        for existing_fso in self.content:
            if type(existing_fso) == t and existing_fso.name == fso.name:
                break
        else:
            fso.parent_dir = self
            self.content.append(fso)

    def content_directories(self):
        return [fso for fso in self.content if is_dir(fso)]

    def walk_dir(self):
        fsos = []
        for fso in self.content:
            fsos.append(fso)
            if is_dir(fso):
                fsos.extend(fso.walk_dir())
        return fsos


class FileSystem:

    def __init__(self):
        self.root_dir = Directory(name="/", parent_dir=None)
        self.pwd = self.root_dir

    def cd(self, dst: str):
        if dst == "..":
            if self.pwd is not self.root_dir:
                self.pwd = self.pwd.parent_dir
        else:
            if dst == self.root_dir.name:
                dst_dir = self.root_dir
            else:
                dst_dir = [dir for dir in self.pwd.content_directories() if dir.name == dst]
                assert len(dst_dir) == 1
                dst_dir = dst_dir[0]
            self.pwd = dst_dir

    def mkdir(self, name: str):
        dir = Directory(name=name, parent_dir=None)
        self.pwd.add_file_system_object(dir)

    def touch(self, name: str, size: int):
        file = File(name=name, parent_dir=None, size=size)
        self.pwd.add_file_system_object(file)

    def walk_fs(self):
        fsos = [self.root_dir]
        fsos.extend(self.root_dir.walk_dir())
        return fsos


def is_dir(fso: FileSystemObject):
    return type(fso) is Directory


def parse_and_run_commands(file_system, lines):
    l_i = 0
    while l_i < len(lines):
        line = lines[l_i]
        l_i += 1
        assert line[0] == "$"
        cmd = line[2:]
        if cmd[:2] == "cd":
            _, dst = cmd.split(" ")
            file_system.cd(dst)
        else:
            # ls mode
            while l_i < len(lines) and lines[l_i][0] != "$":
                output = lines[l_i]
                if output.startswith("dir"):
                    dir_name = output[4:]
                    file_system.mkdir(dir_name)
                else:
                    size, file_name = output.split(" ")
                    file_system.touch(name=file_name, size=int(size))
                l_i += 1


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]

    print("#### Star one ####")
    file_system = FileSystem()
    parse_and_run_commands(file_system, lines)
    dirs = [d for d in file_system.walk_fs() if is_dir(d)]
    dir_sizes = [d.get_size() for d in dirs]
    small_dir_indices = [i for i in range(len(dirs)) if dir_sizes[i] <= 100000]
    total = sum([dir_sizes[i] for i in small_dir_indices])
    print(f"Total: {total}")

    print("#### Star two ####")
    used_space = 70000000 - file_system.root_dir.get_size()
    needed_space = max(0, 30000000 - used_space)
    sorted_dirs = [dirs[i] for i in np.argsort(dir_sizes)]
    for d in sorted_dirs:
        size = d.get_size()
        if size >= needed_space:
            print(f"Delete dir size: {size}")
            break
