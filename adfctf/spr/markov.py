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

def get_player_markov(p):
    player_markov = np.zeros((3,3))


    for i in range(27):
        print(p.recvline().decode(), end="")

    p.sendline("5")
    # for i in range(13):
    #     print(p.recvline().decode(), end="")

    print(p.recvuntil("What is your move?\r\n", drop=True).decode())

    prev_move = -1
    total_games = 0
    opp_moves = []
    while True:
        p.sendline("p")

        p_line = p.recvline().decode()
        if p_line[0] == "*":
            fight = False

        print(p.recvuntil("You chose", drop=True, timeout=5).decode())

        result = p.recvline().decode()
        print(result)
        if result[0] == "-":
            break
        opp_move = MAPPING[result[-4]]
        opp_moves.append(opp_move)
        print(result, end="")
        print(p.recvline().decode(), end="")

        if prev_move != -1:
            total_games += 1
            player_markov[prev_move][opp_move] = player_markov[prev_move][opp_move] + 1

        print("MARKOV")
        print(player_markov)
        prev_move = opp_move

    print(p.recvuntil("8. Samuel Grainger\r\n", drop=True).decode())

    print("FINAL MARKOV")
    print(player_markov)
    print("OPPONENT MOVES")
    print(opp_moves)
    return player_markov, total_games

def exploit(p, player_markov, total_games):
    p.sendline("5")
    print(p.recvuntil("What is your move?\r\n", drop=True).decode())

    move = "p"
    prev_move = -1
    while True:
        p.sendline(move)

        p_line = p.recvline().decode()
        if p_line[0] == "*":
            fight = False

        print(p.recvuntil("You chose", drop=True, timeout=5).decode())

        result = p.recvline().decode()
        print(result)
        if result[0] == "-":
            break
        opp_move = MAPPING[result[-4]]
        pred_next_move = np.argmax(player_markov, axis=1)[opp_move]
        # pred_next_move = random.choices([0,1,2], weights=player_markov[opp_move],k=1)[0]
        print("Predicted Next Move:", pred_next_move)
        move = REVERSE_MAPPING[WINNING_MAPPING[pred_next_move]]
        print("Next Move", move)
        print(result, end="")
        print(p.recvline().decode(), end="")

        if prev_move != -1:
            total_games += 1
            player_markov[prev_move][opp_move] = player_markov[prev_move][opp_move] + 1

        print("MARKOV")
        print(player_markov)
        prev_move = opp_move

    print(p.recvuntil("8. Samuel Grainger\r\n", drop=True).decode())

def main():
    p = remote("spr-championship.ctf.fifthdoma.in", 1700)
    player_markov, total_games = get_player_markov(p)
    exploit(p, player_markov, total_games)

if __name__ == "__main__":
    main()
