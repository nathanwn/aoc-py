from random import randint

chars = [".", ".", ".", "-", "/", "\\", "|"]

m = randint(2, 3)
n = randint(2, 3)

g = []

for i in range(m):
    s = []
    for j in range(n):
        s.append(chars[randint(0, len(chars) - 1)])
    g.append("".join(s))

for ss in g:
    print(ss)
