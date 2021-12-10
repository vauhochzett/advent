import itertools
import sys
import time

t0 = time.perf_counter()

nums = []
with open(sys.argv[1], "r") as f:
    for l in f:
        nums.append(int(l))

t1 = time.perf_counter()

for i, j, k in itertools.combinations(nums, 3):
    if i + j + k == 2020:
        print(i * j * k)
        break

t2 = time.perf_counter()

tf = lambda x: f"{round(x*1000, 5)} ms"

print(
    f"\nTiming\n======\n\nFile read: {tf(t1-t0)}\nAlgo: {tf(t2-t1)}\nTotal: {tf(t2-t0)}"
)
