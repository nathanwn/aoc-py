from random import randint

print("seeds: ", end='')

for i in range(10):
    print(f"{randint(1, 200)} {randint(1, 200)}", end=" ")

print("\n")

for j in range(5):
    print("foo:")
    s = set()

    while len(s) < 30:
        s.add(randint(1, 300))
    ss = list(s)
    ss.sort()

    for i in range(0, len(ss), 2):
        print(f"{int(100 ** (i / 2))} {ss[i]} {ss[i + 1] - ss[i] + 1}")
    print()
