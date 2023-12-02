import argparse


def parse_round(round_input) -> tuple[int, int, int]:
    red = 0
    green = 0
    blue = 0

    color_inputs = [_.strip() for _ in round_input.split(",")]
    for color_input in color_inputs:
        num_input, color = color_input.split()
        num = int(num_input)
        if color == "red":
            red = num
        elif color == "green":
            green = num
        elif color == "blue":
            blue = num
        else:
            assert False

    return (red, green, blue)


def parse_game(line: str) -> list[tuple[int, int, int]]:
    round_inputs = [_.strip() for _ in line.split(":")[1].strip().split(";")]
    rounds = []
    for round_input in round_inputs:
        rounds.append(parse_round(round_input))
    return rounds


def validate_game(game: list[tuple[int, int, int]]) -> bool:
    for round in game:
        if round[0] > 12 or round[1] > 13 or round[2] > 14:
            return False
    return True


def solve_game(game: list[tuple[int, int, int]]) -> int:
    max_each = [0, 0, 0]
    for round in game:
        for i in range(3):
            if max_each[i] < round[i]:
                max_each[i] = round[i]
    return max_each[0] * max_each[1] * max_each[2]


def part1(lines: list[str]):
    ans = 0

    for i, line in enumerate(lines):
        game = parse_game(line)
        if validate_game(game):
            ans += i + 1

    return ans


def part2(lines: list[str]):
    ans = 0

    for i, line in enumerate(lines):
        game = parse_game(line)
        ans += solve_game(game)

    return ans


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
