from __future__ import division
import socket
from pwn import *
import random
import itertools
import string

RHOST = "spr-championship.ctf.fifthdoma.in"
RPORT = 1700


en_choices = {"p": 0, "s": 0, "r": 0}
en_responses_own = {}
en_responses_mine = {}
wlr = {"w": 0, "l": 0, "d": 0}

MAP0 = {
    "R" : 0,
    "P" : 1,
    "S" : 2
}

MAP1 = {
    "S" : 0,
    "P" : 1,
    "R" : 2
}

MAP2 = {
    "R" : 1,
    "P" : 2,
    "S" : 0
}

base_3 = lambda xyz: xyz[2]*3**2 + xyz[1]*3 + xyz[0]

def main():
    NUM_ROUNDS = 5
    input = ""
    max_rounds = 6399
    ternary_bin0 = []
    ternary_bin1 = []
    ternary_bin2 = []
    string_0 = ""
    for j in range(NUM_ROUNDS):
        s = remote(RHOST,RPORT)

        s.recvuntil("Grainger").decode()
        s.sendline("8")
        s.recvuntil("move?").decode()
        rounds_played = 0
        while rounds_played < max_rounds:
            s.recv(4096).decode()


            if input == "":
                    score  = {'RR': 0, 'PP': 0, 'SS': 0, \
                              'PR': 1, 'RS': 1, 'SP': 1, \
                              'RP': -1, 'SR': -1, 'PS': -1,}
                    cscore = {'RR': 'r', 'PP': 'r', 'SS': 'r', \
                              'PR': 'b', 'RS': 'b', 'SP': 'b', \
                              'RP': 'c', 'SR': 'c', 'PS': 'c',}
                    beat = {'P': 'S', 'S': 'R', 'R': 'P'}
                    cede = {'P': 'R', 'S': 'P', 'R': 'S'}
                    rps = ['R', 'P', 'S']
                    wlt = {1:0,-1:1,0:2}

                    def counter_prob(probs):
                            weighted_list = []
                            for h in rps:
                                    weighted = 0
                                    for p in probs.keys():
                                            points = score[h+p]
                                            prob = probs[p]
                                            weighted += points * prob
                                    weighted_list.append((h, weighted))

                            return max(weighted_list, key=operator.itemgetter(1))[0]

                    played_probs = defaultdict(lambda: 1)
                    dna_probs = [defaultdict(lambda: defaultdict(lambda: 1)) for i in range(18)]

                    wlt_probs = [defaultdict(lambda: 1) for i in range(9)]

                    answers = [{'c': 1, 'b': 1, 'r': 1} for i in range(12)]

                    patterndict = [defaultdict(str) for i in range(6)]

                    consec_strat_usage = [[0]*6,[0]*6,[0]*6] #consecutive strategy usage
                    consec_strat_candy = [[],   [],   []   ] #consecutive strategy candidates

                    output = random.choice(rps)
                    histories = ["","",""]
                    dna = ["" for i in range(12)]

                    sc = 0
                    strats = [[] for i in range(3)]
            else:
                    prev_sc = sc

                    sc = score[output + input]
                    for j in range(3):
                            prev_strats = strats[j][:]
                            for i, c in enumerate(consec_strat_candy[j]):
                                    if c == input:
                                            consec_strat_usage[j][i] += 1
                                    else:
                                            consec_strat_usage[j][i] = 0
                            m = max(consec_strat_usage[j])
                            strats[j] = [i for i, c in enumerate(consec_strat_candy[j]) if consec_strat_usage[j][i] == m]

                            for s1 in prev_strats:
                                    for s2 in strats[j]:
                                            wlt_probs[j*3+wlt[prev_sc]][chr(s1)+chr(s2)] += 1

                            if dna[2*j+0] and dna[2*j+1]:
                                    answers[2*j+0][cscore[input+dna[2*j+0]]] += 1
                                    answers[2*j+1][cscore[input+dna[2*j+1]]] += 1
                            if dna[2*j+6] and dna[2*j+7]:
                                    answers[2*j+6][cscore[input+dna[2*j+6]]] += 1
                                    answers[2*j+7][cscore[input+dna[2*j+7]]] += 1

                            for length in range(min(10, len(histories[j])), 0, -2):
                                    pattern = patterndict[2*j][histories[j][-length:]]
                                    if pattern:
                                            for length2 in range(min(10, len(pattern)), 0, -2):
                                                    patterndict[2*j+1][pattern[-length2:]] += output + input
                                    patterndict[2*j][histories[j][-length:]] += output + input
                    played_probs[input] += 1
                    dna_probs[0][dna[0]][input] +=1
                    dna_probs[1][dna[1]][input] +=1
                    dna_probs[2][dna[1]+dna[0]][input] +=1
                    dna_probs[9][dna[6]][input] +=1
                    dna_probs[10][dna[6]][input] +=1
                    dna_probs[11][dna[7]+dna[6]][input] +=1

                    histories[0] += output + input
                    histories[1] += input
                    histories[2] += output

                    dna = ["" for i in range(12)]
                    for j in range(3):
                            for length in range(min(10, len(histories[j])), 0, -2):
                                    pattern = patterndict[2*j][histories[j][-length:]]
                                    if pattern != "":
                                            dna[2*j+1] = pattern[-2]
                                            dna[2*j+0]  = pattern[-1]
                                            for length2 in range(min(10, len(pattern)), 0, -2):
                                                    pattern2 = patterndict[2*j+1][pattern[-length2:]]
                                                    if pattern2 != "":
                                                            dna[2*j+7] = pattern2[-2]
                                                            dna[2*j+6] = pattern2[-1]
                                                            break
                                            break

                    probs = {}
                    for hand in rps:
                            probs[hand] = played_probs[hand]

                    for j in range(3):
                            if dna[j*2] and dna[j*2+1]:
                                    for hand in rps:
                                            probs[hand] *= dna_probs[j*3+0][dna[j*2+0]][hand] * \
                                                           dna_probs[j*3+1][dna[j*2+1]][hand] * \
                                                                       dna_probs[j*3+2][dna[j*2+1]+dna[j*2+0]][hand]
                                            probs[hand] *= answers[j*2+0][cscore[hand+dna[j*2+0]]] * \
                                                           answers[j*2+1][cscore[hand+dna[j*2+1]]]
                                    consec_strat_candy[j] = [dna[j*2+0], beat[dna[j*2+0]], cede[dna[j*2+0]],\
                                                             dna[j*2+1], beat[dna[j*2+1]], cede[dna[j*2+1]]]
                                    strats_for_hand = {'R': [], 'P': [], 'S': []}
                                    for i, c in enumerate(consec_strat_candy[j]):
                                            strats_for_hand[c].append(i)
                                    pr = wlt_probs[wlt[sc]+3*j]
                                    for hand in rps:
                                            for s1 in strats[j]:
                                                    for s2 in strats_for_hand[hand]:
                                                            probs[hand] *= pr[chr(s1)+chr(s2)]
                            else:
                                    consec_strat_candy[j] = []
                    for j in range(3):
                            if dna[j*2+6] and dna[j*2+7]:
                                    for hand in rps:
                                            probs[hand] *= dna_probs[j*3+9][dna[j*2+6]][hand] * \
                                                           dna_probs[j*3+10][dna[j*2+7]][hand] * \
                                                                       dna_probs[j*3+11][dna[j*2+7]+dna[j*2+6]][hand]
                                            probs[hand] *= answers[j*2+6][cscore[hand+dna[j*2+6]]] * \
                                                           answers[j*2+7][cscore[hand+dna[j*2+7]]]

                    output = counter_prob(probs)



            s.sendline(output)
            resp = s.recvuntil("move?").decode().split("\r\n")
            # print(resp)
            result = resp[1].strip('.').split()[-1][0]
            if result == "w" or result == "l":
                rounds_played += 1

            input = resp[2][-2].upper()

            string_0 = string_0 + input
            print(resp)
            print(string_0)



        with open("string_0_raw.txt", "w") as f:
            f.write(string_0)

        s.interactive()

if __name__ == "__main__":
    main()
