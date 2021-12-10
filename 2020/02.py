import sys
import time
from typing import Tuple


def segment(l: str) -> Tuple[int, int, str, str]:
    segments = l.split(": ")
    count, letter = segments[0].split(" ")
    count_min, count_max = [int(s) for s in count.split("-")]
    pswd = segments[1]
    return count_min, count_max, letter, pswd


def is_valid_1(l: str):
    # 2-5 l: fllxf
    count_min, count_max, letter, pswd = segment(l)
    count_letter = pswd.count(letter)
    return count_min <= count_letter <= count_max


def is_valid_2(l: str):
    # 2-5 l: fllxf
    # Exactly one of the positions needs to contain the letter
    pos_1, pos_2, letter, pswd = segment(l)
    idx_1 = pos_1 - 1
    idx_2 = pos_2 - 1
    return (pswd[idx_1] == letter) ^ (pswd[idx_2] == letter)


t0 = time.perf_counter()

valid = 0
with open(sys.argv[1], "r") as f:
    for l in f:
        valid += is_valid_2(l)

t1 = time.perf_counter()

print(f"Valid: {valid}\n\nTime: {(t1-t0)*1000} ms")
