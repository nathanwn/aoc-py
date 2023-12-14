import argparse


def score(win: list[int], have: list[int]) -> int:
    s = 0
    for x in have:
        if x in win:
            s += 1
    return s


def parse_line(line: str) -> tuple[list[int], list[int]]:
    _, _, nums = line.partition(":")
    win_nums, _, have_nums = nums.partition("|")
    win = list(map(lambda _: int(_), win_nums.strip().split()))
    have = list(map(lambda _: int(_), have_nums.strip().split()))
    return win, have


def part1(input: list[str]) -> int:
    ans = 0
    for line in input:
        win, have = parse_line(line)
        s = score(win, have)
        ans += 0 if s == 0 else (1 << (s - 1))
    return ans


def part2(input: list[str]):
    cnt = [1 for _ in range(len(input))]
    for i, line in enumerate(input):
        win, have = parse_line(line)
        s = score(win, have)
        for j in range(i + 1, min(i + s + 1, len(input))):
            cnt[j] += cnt[i]
    return sum(cnt)


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
