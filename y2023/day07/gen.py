from random import randint

CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def random_hand() -> str:
    cards = [CARDS[randint(0, len(CARDS) - 1)] for i in range(5)]
    return "".join(cards)


for i in range(3):
    print(f"{random_hand()} {randint(1, 10)}")
