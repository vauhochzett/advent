import re
import sys
import time
from typing import Any, Callable, Dict, List

# Handheld Halting
#
# Operations
# acc = inc/dec global value `accumulator` by argument
# jmp = jump to instruction relative to current position
# nop = do nothing


class Instruction:
    def __init__(self, operation: str, value: int, executed: bool = False) -> None:
        self.operation = operation
        self.value = value
        self.executed = executed


# GLOBALS
accumulator: int = 0
program: List[Instruction] = []
instructions_executed: List[int] = []

# Run the program until it reaches the same instruction a second time.
# Terminate and print accumulator value


def parse_instruction(instruction_line: str) -> Instruction:
    # nop +0
    m = re.fullmatch(r"(\w+) (\+|-)(\d+)\n", instruction_line)
    if not m:
        raise ValueError(f"Invalid instruction: {instruction_line}")

    ins: str
    sgn: str
    num_us: str
    ins, sgn, num_us = m.groups()

    num: int = int(num_us)
    if sgn == "-":
        num = -num

    return Instruction(operation=ins, value=num)


def execute(pointer: int) -> int:
    global accumulator
    global program

    instruction: Instruction = program[pointer]
    # Mark executed
    program[pointer].executed = True

    if instruction.operation == "nop":
        return 1 + pointer
    elif instruction.operation == "jmp":
        return instruction.value + pointer
    elif instruction.operation == "acc":
        accumulator += instruction.value
        return 1 + pointer
    else:
        raise ValueError(f"Unknown operation: {instruction.operation}")


def _roll_back_instruction(pointer: int) -> None:
    global program
    global accumulator

    instruction: Instruction = program[pointer]

    if instruction.operation == "acc":
        # Reverse accumulation
        accumulator -= instruction.value

    program[pointer].executed = False


def roll_back(condition: Callable[[int], bool]):
    """ Roll back the state until the given condition is met based on the passed pointer. """

    global instructions_executed

    pointer: int
    # We assume that one instruction can always be safely rolled back.
    while True:
        # Always roll back pointer and remove executed instruction from list
        pointer = instructions_executed.pop(-1)
        # Reverse accumulation and reset hit_detector
        _roll_back_instruction(pointer)

        # Stop if condition is met
        if condition(pointer):
            break

    # Hit the state before the last unchanged jmp or nop

    # The instruction currently pointed to was rolled back
    return pointer


def swap_jmp_nop(pointer: int):
    """ Swap the instruction the pointer points to. """

    ins: Instruction = program[pointer]

    if ins.operation == "jmp":
        ins.operation = "nop"
    elif ins.operation == "nop":
        ins.operation = "jmp"
    else:
        raise ValueError(f"Tried to swap {ins.operation}")


t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    for l in f:
        instruction = parse_instruction(l)
        program.append(instruction)

t1 = time.perf_counter()

instruction_index: int = 0
code_changed: bool = False  # Was an instruction changed, and if yes, which?
past_changes: List[int] = []  # Changed indices that did not fix the infinite loop

state: Dict[str, Any] = {}

while True:
    # Successfull termination
    if instruction_index >= len(program):
        break

    if program[instruction_index].executed:
        # If a change was tried, we first need to revert back to the state before it was changed
        if code_changed:
            # Revert change again
            swap_jmp_nop(past_changes[-1])
            code_changed = False

            # Go back to state before the change was tried
            instruction_index = roll_back(lambda p: p == past_changes[-1])

            # Continue rolling back from the point of the unsuccessful change

        # Roll back until first untried jmp or nop
        instruction_index = roll_back(
            lambda p: program[p].operation in ["jmp", "nop"] and p not in past_changes
        )
        # Change position
        swap_jmp_nop(instruction_index)
        code_changed = True
        past_changes.append(instruction_index)

        # Continue running

    instructions_executed.append(instruction_index)
    instruction_index = execute(instruction_index)

t2 = time.perf_counter()


from util import tf

print(
    f"Accumulator value: {accumulator}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Execute: {tf(t2-t1)}\n"
    f"=========\n"
    f"Total: {tf(t2-t0)}"
)
