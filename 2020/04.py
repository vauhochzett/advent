import re
import sys
import time
from typing import Dict, List

# Expected fields + validation rules:
#
# - byr (Birth Year) - four digits; at least 1920 and at most 2002.
# - iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# - eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# - hgt (Height) - a number followed by either cm or in:
#       + If cm, the number must be at least 150 and at most 193.
#       + If in, the number must be at least 59 and at most 76.
# - hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# - ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# - pid (Passport ID) - a nine-digit number, including leading zeroes.
# - [IGNORE] cid (Country ID) - ignored, missing or not.


req_fields: List[str] = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def get_fields(passport: str) -> Dict[str, str]:
    field_dict: Dict[str, str] = dict()
    for field in re.findall(r"\w+:[^\s]+", passport):
        k, v = field.split(":")
        field_dict[k] = v
    return field_dict


def is_valid(passport: str) -> bool:
    fields: Dict[str, str] = get_fields(passport)

    # All fields are required
    if any([rf not in fields for rf in req_fields]):
        return False

    # byr, iy3, eyr (1) need to be digits
    try:
        byr: int = int(fields["byr"])
        iyr: int = int(fields["iyr"])
        eyr: int = int(fields["eyr"])
    except ValueError:
        return False

    # byr (2) in [1920, 2002]
    # iyr (2) in [2010, 2020]
    # eyr (2) in [2020, 2030]
    if not all(
        [
            a <= y <= b
            for y, a, b in [(byr, 1920, 2002), (iyr, 2010, 2020), (eyr, 2020, 2030)]
        ]
    ):
        return False

    # hgt (1) parse: number + "cm" or "in"
    match = re.fullmatch(r"(\d+)(cm|in)", fields["hgt"])
    if not match:
        return False
    # hgt (2) allowed values
    hgt = int(match.group(1))
    unit = match.group(2)
    if (unit == "cm" and not (150 <= hgt <= 193)) or (
        unit == "in" and not (59 <= hgt <= 76)
    ):
        return False

    # hcl (1) needs to match pattern
    if not re.fullmatch(r"#[0-9a-f]{6}", fields["hcl"]):
        return False

    # ecl (1) valid values
    if not fields["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False

    # pid (1) nine digits including leading zeroes
    if not re.fullmatch(r"\d{9}", fields["pid"]):
        return False

    return True


t0 = time.perf_counter()

valid: int = 0

with open(sys.argv[1], "r") as f:
    passport: str = ""
    for l in f:
        if l == "\n":
            if is_valid(passport):
                valid += 1
            passport = ""
            continue

        passport += l[:-1] + " "

    # Don't forget the last passport
    if is_valid(passport):
        valid += 1


t1 = time.perf_counter()


# Count the number of valid passports - those that have all required fields.
# Treat cid as optional.
# In your batch file, how many passports are valid?

from util import tf

print(f"Valid: {valid}\n\n" f"Time taken: {tf(t1-t0)}")
