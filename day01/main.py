import argparse


num_words = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def index(s: str, sub: str) -> int:
    """Alternative implementation of ``str.index`` that does not raise error
    when the substring is not found and returns ``len(s)`` instead.
    """
    return s.index(sub) if sub in s else len(s)


def rindex(s: str, sub: str) -> int:
    """Alternative implementation of ``str.rindex`` that does not raise error
    when the substring is not found and returns ``-1`` instead.
    """
    return s.rindex(sub) if sub in s else -1


def solve_line_1(line: str) -> int:
    first_positions = [index(line, str(i)) for i in range(10)]

    first_digit = 0
    first_pos = len(line)

    for i, pos in enumerate(first_positions):
        if pos < first_pos:
            first_pos = pos
            first_digit = i

    last_positions = [rindex(line, str(i)) for i in range(10)]
    last_digit = 0
    last_pos = -1

    for i, pos in enumerate(last_positions):
        if pos > last_pos:
            last_pos = pos
            last_digit = i

    return first_digit * 10 + last_digit


def solve_line_2(line: str) -> int:
    first_positions_of_digits = [index(line, str(i)) for i in range(10)]
    first_positions_of_words = [index(line, num_words[i]) for i in range(10)]
    first_positions = [
        min(first_positions_of_digits[i], first_positions_of_words[i])
        for i in range(10)
    ]

    first_digit = 0
    first_pos = len(line)

    for i, pos in enumerate(first_positions):
        if pos < first_pos:
            first_pos = pos
            first_digit = i

    last_positions_of_digits = [rindex(line, str(i)) for i in range(10)]
    last_positions_of_words = [rindex(line, num_words[i]) for i in range(10)]
    last_positions = [
        max(last_positions_of_digits[i], last_positions_of_words[i]) for i in range(10)
    ]
    last_digit = 0
    last_pos = -1

    for i, pos in enumerate(last_positions):
        if pos > last_pos:
            last_pos = pos
            last_digit = i

    return first_digit * 10 + last_digit


def get_first_num_char(line: str) -> int:
    first_pos = [-1 for _ in range(10)]

    for i in range(10):
        first_pos[i] = line.find(str(i))

    smallest_first_pos = len(line)
    first_num = 0

    for i in range(10):
        if first_pos[i] < smallest_first_pos:
            smallest_first_pos = first_pos[i]
            first_num = i

    return first_num


def get_last_num_char(line: str) -> int:
    last_char_pos = [-1 for _ in range(10)]

    for i in range(10):
        last_char_pos[i] = line.rfind(str(i))

    largest_last_pos = -1
    last_num = 0

    for i in range(10):
        if last_char_pos[i] < largest_last_pos:
            largest_last_pos = last_char_pos[i]
            last_num = i

    return last_num


def part1(lines: list[str]):
    s = 0
    for line in lines:
        num = solve_line_1(line)
        s += num
    return s


def part2(lines: list[str]):
    s = 0
    for line in lines:
        num = solve_line_2(line)
        s += num
    return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2"])
    parser.add_argument("input_file")

    args = parser.parse_args()

    with open(args.input_file, mode="r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    if args.part == "1":
        print(f"Part 1: {part1(lines)}")
    else:
        print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main()
