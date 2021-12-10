import sys
import time
from collections import Counter
from typing import List

# Adapter Array
#
# - List of joltage adapters
# - Can take inputs of 1-3 jolts below their rated joltage
# - In addition, the device can take a joltage of max(joltages) + 3
# - Charging outlet has rating of 0

# A) Find a chain that connects all adapters from the socket (0) to the device (max + 3)
#    and multiply the number of 1-jolt steps with the number of 3-jolt steps.

adapters: List[int] = []

t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    for l in f:
        adapters.append(int(l[:-1]))

# end / device = max+3
device: int = max(adapters) + 3

t1 = time.perf_counter()

adapters.sort()

# Part 1


def count_joltage_steps(adapters: List[int]) -> int:
    deltas: Counter = Counter({x: 0 for x in [1, 2, 3]})
    last_adapter: int = 0

    for next_adapter in adapters:
        delta: int = next_adapter - last_adapter
        if delta not in deltas:
            raise ValueError(f"Delta of {delta} found: {next_adapter} - {last_adapter}")

        deltas[delta] += 1
        last_adapter = next_adapter

    return deltas[1] * deltas[3]


joltage_step_result: int = count_joltage_steps(adapters + [device])

# B) Find all possible chains that connect the socket to the device
#    and count the number of distinct chains.

# Part 2

t2 = time.perf_counter()


def count_chain_graph(adapters: List[int], start: int, end: int) -> int:
    """ Count chains based on a graph. Assumes adapters list is sorted. """
    adapters = [start] + adapters + [end]
    valid_path_count: List[int] = [0] * len(adapters)

    # There is one valid path "to" the start
    valid_path_count[0] = 1

    for i in range(1, len(adapters)):
        adp: int = adapters[i]
        paths_to_self: int = 0

        for j in range(i - 1, -1, -1):
            prev: int = adapters[j]
            # First non-match means we found all valid paths
            if (adp - prev) not in [1, 2, 3]:
                break
            paths_to_self += valid_path_count[j]

        # Done counting valid paths
        valid_path_count[i] = paths_to_self

    return valid_path_count[-1]


chain_count: int = count_chain_graph(adapters, start=0, end=device)

t3 = time.perf_counter()


from util import tf

print(
    f"Part 1: Joltage steps = {joltage_step_result}\n"
    f"Part 2: Number of distinct chains = {chain_count}\n"
    f"\n"
    f"Parse file and collect adapters: {tf(t1-t0)}\n"
    f"Count joltage steps: {tf(t2-t1)}\n"
    f"Count chains: {tf(t3-t2)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)
