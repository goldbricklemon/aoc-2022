# -*- coding: utf-8 -*-


def search_marker_position(stream, marker_length):
    for i in range(marker_length - 1, len(stream)):
        packet = stream[i - marker_length + 1: i + 1]
        unique_chars = True
        for c_i, character in enumerate(packet):
            tmp_packet = packet[:c_i] + packet[c_i + 1:]
            if character in tmp_packet:
                unique_chars = False
                break
        if unique_chars:
            return i + 1
    return None


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        line = f.readline()
    stream = line.strip("\n").strip("\r")

    print("#### Star one ####")
    marker_position = search_marker_position(stream, marker_length=4)
    print(f"Marker position: {marker_position}")

    print("#### Star two ####")
    marker_position = search_marker_position(stream, marker_length=14)
    print(f"Marker position: {marker_position}")
