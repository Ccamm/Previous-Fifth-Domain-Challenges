from pwn import *
import numpy as np
import random

MAPPING = {
    "r" : 0,
    "p" : 1,
    "s" : 2
}

REVERSE_MAPPING = {
    0 : "r",
    1 : "p",
    2 : "s"
}

WINNING_MAPPING = {
    0 : 1,
    1 : 2,
    2 : 0
}
# Markov Matrix Format
#
#       r p s
# 0 : r
# 1 : p
# 2 : s

PLAYER_MOVES = [2, 1, 0, 2, 2, 1, 0, 1, 1, 2, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 1, 0, 0, 0, 2, 0, 0, 2, 1, 0, 0, 2, 0, 1, 2, 2, 1, 2, 1, 0, 1, 0, 2, 1, 1, 2, 2, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 1, 2, 0, 2, 0, 2, 1, 2, 0, 0, 1, 1, 2, 0, 2, 1, 2, 1, 2, 2, 0, 0, 2, 1, 2, 1, 2, 0, 1, 2, 1, 2, 2, 1, 0, 1, 1, 0, 2, 0, 2, 0, 0, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 1, 2, 2, 1, 0, 1, 0, 1, 2, 1, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 2, 0, 0, 0, 1, 2, 2, 2, 1, 0, 2, 1, 1, 0, 2, 2, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 1, 2, 2, 2, 0, 1, 1, 0, 0, 1, 2, 0, 0, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 0, 2, 0, 2, 1, 2, 0, 1, 2, 0, 1, 0, 1, 2, 0, 2, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 0, 0, 2, 1, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 2, 1, 0, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 2, 0, 2, 2, 1, 0, 0, 2, 1, 0, 1, 0, 2, 2, 0, 1, 1, 0, 2, 2, 1, 2, 1, 2, 1, 1, 1, 0, 0, 2, 0, 1, 2, 0, 0, 2, 0, 0, 0, 2]

def get_seed(opp_moves):
    seed = -1
    for i in range(500000):
        print("testing seed:", i)
        random.seed(i)

        seed = -1
        for x in range(len(opp_moves)):
            random_int = random.randint(0,2)
            if random_int == opp_moves[x]:
                seed = i
            else:
                seed = -1
                break

        if seed != -1:
            print("FOUND THE SEED:", seed)
            break

    print("NO SEED FOUND :(")
    print("Initialising Random Number Generator")

    random.seed(seed)
    for x in range(len(opp_moves)):
        random.randint(0,2)


def exploit(p):

    for i in range(27):
        print(p.recvline().decode(), end="")

    p.sendline("3")
    # for i in range(13):
    #     print(p.recvline().decode(), end="")

    print(p.recvuntil("What is your move?\r\n", drop=True).decode())

    prev_move = -1
    total_games = 0
    opp_moves = []
    i = 0
    while True:
        if i < 2:
            p.sendline("p")
        else:
            p.sendline(
                REVERSE_MAPPING[WINNING_MAPPING[PLAYER_MOVES[i]]]
            )

        p_line = p.recvline().decode()
        if p_line[0] == "*":
            fight = False

        # if total_games == 20:
        #     get_seed(opp_moves)

        print(p.recvuntil("You chose", drop=True, timeout=5).decode())

        result = p.recvline().decode()
        print(result)
        if result[0] == "-":
            break
        opp_move = MAPPING[result[-4]]
        opp_moves.append(opp_move)
        print(result, end="")
        print(p.recvline().decode(), end="")
        total_games += 1
        i += 1


    print(p.recvuntil("8. Samuel Grainger\r\n", drop=True).decode())

    print(opp_moves)

def main():
    p = remote("spr-championship.ctf.fifthdoma.in", 1700)
    seed = exploit(p)

if __name__ == "__main__":
    main()
