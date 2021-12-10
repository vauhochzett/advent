import re
import sys
import time
from collections import Counter
from typing import Dict, List, Tuple, Union, cast

# pylint: disable=unsubscriptable-object

# Docking Data
#
# Puzzle input: Initialization program
#   - Can update bitmask or write value to memory
#   - Values / memory addresses: 36-bit unsigned int
#   - mem[8] = 11
#   - Bitmask:
#       + 36-length string, Big Endian (most significant first)
#       + X = do nothing, 1/0 = overwrite

t0 = time.perf_counter()

commands: List[Union[str, Tuple[int, int]]] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        if l.startswith("mask"):
            commands.append(l[7:-1])
            continue

        m = re.fullmatch(r"mem\[(\d+)\] = (\d+)\n", l)
        if not m:
            raise ValueError()

        address: int
        value: int
        address, value = [int(x) for x in m.groups()]
        commands.append((address, value))

t1 = time.perf_counter()


class Memory:
    def __init__(self) -> None:
        self.max: str = ""
        # Default value for any key in a Counter is 0, which means we can easily sum up later.
        self.container: Counter[int] = Counter()

    def _int_to_maskable_str(self, val: int) -> List[str]:
        value_bin: str = bin(val)
        value_zfilled: str = (value_bin[2:]).zfill(len(self.mask))
        return list(value_zfilled)

    def update_mask(self, mask: str) -> None:
        self.mask = mask

    def write(self, address: int, value: int) -> None:
        raise NotImplementedError("Abstract method")

    def sum(self) -> int:
        return sum(self.container.values())


# Part 1: Mask overwrites values at indices


class MemoryPt1(Memory):
    def __init__(self) -> None:
        super().__init__()

    def _apply_mask(self, value: int) -> int:
        value_list: List[str] = self._int_to_maskable_str(value)

        for i, c in enumerate(self.mask):
            if c != "X":
                value_list[i] = c

        return int("".join(value_list), 2)

    def write(self, address: int, value: int) -> None:
        value = self._apply_mask(value=value)
        self.container[address] = value


# Part 2: Mask serves as memory address decoder


class MemoryPt2(Memory):
    def __init__(self) -> None:
        super().__init__()

    def _apply_mask(self, address: int) -> List[str]:
        # bit = 0 => corresponding bit is unchanged
        # bit = 1 => overwrite bit with 1
        # bit = X => corresponding bit is FLOATING

        # FLOATING bit:
        # - fluctuates
        # - can take all possible values
        # ==> multiple target addresses

        address_listed: List[str] = self._int_to_maskable_str(address)

        for i, c in enumerate(self.mask):
            if c in "1X":
                address_listed[i] = c
            elif c != "0":
                raise ValueError(f"Invalid char: {c}")

        return address_listed

    def write(self, address: int, value: int) -> None:
        addresses_base: List[str] = self._apply_mask(address=address)
        addresses: List[List[str]] = [[]]

        for a in addresses_base:
            for i in range(len(addresses)):
                if a in "01":
                    addresses[i].append(a)
                elif a == "X":
                    addresses.append(addresses[i] + ["0"])
                    addresses[i].append("1")
                else:
                    raise ValueError(f"Unknown value: {a}")

        for target in [int("".join(a), 2) for a in addresses]:
            self.container[target] = value


def execute_instructions(
    memory: Memory, commands: List[Union[str, Tuple[int, int]]]
) -> int:
    for command in commands:
        if isinstance(command, str):
            command = cast(str, command)
            memory.update_mask(command)
        elif type(command) is tuple:
            command = cast(Tuple[int, int], command)
            memory.write(*command)
        else:
            raise ValueError(f"Invalid type: {type(command)}")

    return memory.sum()


# Part 1:
memory1: Memory = MemoryPt1()
mem_sum_1: int = execute_instructions(memory=memory1, commands=commands)

t2 = time.perf_counter()

# Part 2:
memory2: Memory = MemoryPt2()
mem_sum_2: int = execute_instructions(memory=memory2, commands=commands)

t3 = time.perf_counter()


from util import tf

print(
    f"Part 1: Sum = {mem_sum_1}\n"
    f"Part 2: Sum = {mem_sum_2}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Part 1: Calculate sum: {tf(t2-t1)}\n"
    f"Part 2: Calculate sum: {tf(t3-t2)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)
