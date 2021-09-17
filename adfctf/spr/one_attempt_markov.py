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
CUTOFF_INIT = 0.9
CUTOFF_STEP = 0.1

def pick_next_move(player_markov, opp_move, cutoffs):
    pred_next_move = np.argmax(player_markov, axis=1)[opp_move]
    max_counts = player_markov[opp_move][pred_next_move]
    top_chosen_moves = np.where(
        player_markov[opp_move] > max_counts*cutoffs[opp_move]
    )[0]

    if top_chosen_moves.shape[0] == 2:
        for x in top_chosen_moves:
            if WINNING_MAPPING[x] in top_chosen_moves:
                return REVERSE_MAPPING[WINNING_MAPPING[x]]

    return REVERSE_MAPPING[WINNING_MAPPING[pred_next_move]]

def get_player_markov(p):

    player_markov = np.zeros((3,3))
    cutoffs = 3*[CUTOFF_INIT]
    cutoff_adj = 3*[1]


    for i in range(27):
        print(p.recvline().decode(), end="")

    p.sendline("7")
    # for i in range(13):
    #     print(p.recvline().decode(), end="")

    print(p.recvuntil("What is your move?\r\n", drop=True).decode())

    prev_move = -1
    total_games = 0
    opp_moves = []
    opp_move = 0
    while True:

        move = pick_next_move(player_markov, opp_move, cutoffs)
        # pred_next_move = np.argmax(player_markov, axis=1)[opp_move]
        # # pred_next_move = random.choices([0,1,2], weights=player_markov[opp_move],k=1)[0]
        # move = REVERSE_MAPPING[WINNING_MAPPING[pred_next_move]]
        p.sendline(move)

        p_line = p.recvline().decode()
        if p_line[0] == "*":
            break

        result = p.recvuntil(".", drop=True, timeout=5).decode()
        if total_games > 100:
            if "won" in result:

                cutoffs[prev_move] = cutoffs[prev_move] + CUTOFF_STEP/cutoff_adj[prev_move]
                cutoff_adj[prev_move] = cutoff_adj[prev_move] + 1
            elif "lost" in result:
                cutoffs[prev_move] = cutoffs[prev_move] - CUTOFF_STEP/cutoff_adj[prev_move]
                cutoff_adj[prev_move] = cutoff_adj[prev_move] + 1

        print(result)
        print(p.recvuntil("You chose", drop=True, timeout=5).decode())

        result = p.recvline().decode()
        print(result)
        if result[0] == "-":
            break
        try:
            opp_move = MAPPING[result[-4]]
        except:
            break
        opp_moves.append(opp_move)
        print(result, end="")
        print(p.recvline().decode(), end="")

        if prev_move != -1:
            total_games += 1
            player_markov[prev_move][opp_move] = player_markov[prev_move][opp_move] + 1

        print("MARKOV")
        print(player_markov)
        prev_move = opp_move
        print("CUTOFFS")
        print(cutoffs)

    print(p.recvuntil("8. Samuel Grainger\r\n", drop=True).decode())

    print("FINAL MARKOV")
    print(player_markov)
    # print("OPPONENT MOVES")
    # print(opp_moves)
    return player_markov, total_games

def main():
    p = remote("spr-championship.ctf.fifthdoma.in", 1700)
    player_markov, total_games = get_player_markov(p)

if __name__ == "__main__":
    main()
