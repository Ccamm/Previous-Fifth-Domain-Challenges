g1 = [2, 1, 0, 2, 2, 1, 0, 1, 1, 2, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 1, 0, 0, 0, 2, 0, 0, 2, 1, 0, 0, 2, 0, 1, 2, 2, 1, 2, 1, 0, 1, 0, 2, 1, 1, 2, 2, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 1, 2, 0, 2, 0, 2, 1, 2, 0, 0, 1, 1, 2, 0, 2, 1, 2, 1, 2, 2, 0, 0, 2, 1, 2, 1, 2, 0, 1, 2, 1, 2, 2, 1, 0, 1, 1, 0, 2, 0, 2, 0, 0, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 1, 2, 2, 1, 0, 1, 0, 1, 2, 1, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 2, 0, 0, 0, 1, 2, 2, 2, 1, 0, 2, 1, 1, 0, 2, 2, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 1, 2, 2, 2, 0, 1, 1, 0, 0, 1, 2, 0, 0, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 0, 2, 0, 2, 1, 2, 0, 1, 2, 0, 1, 0, 1, 2, 0, 2, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 0, 0, 2, 1, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 2, 1, 0, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 2, 0, 2, 2, 1, 0, 0, 2, 1, 0, 1, 0, 2, 2, 0, 1, 1, 0, 2, 2, 1, 2, 1, 2, 1, 1, 1, 0, 0, 2, 0, 1, 2, 0, 0, 2, 0, 0, 0, 2]
g2 = [2, 1, 0, 2, 2, 1, 0, 1, 1, 2, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 1, 0, 0, 0, 2, 0, 0, 2, 1, 0, 0, 2, 0, 1, 2, 2, 1, 2, 1, 0, 1, 0, 2, 1, 1, 2, 2, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 1, 2, 0, 2, 0, 2, 1, 2, 0, 0, 1, 1, 2, 0, 2, 1, 2, 1, 2, 2, 0, 0, 2, 1, 2, 1, 2, 0, 1, 2, 1, 2, 2, 1, 0, 1, 1, 0, 2, 0, 2, 0, 0, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 1, 2, 2, 1, 0, 1, 0, 1, 2, 1, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 2, 0, 0, 0, 1, 2, 2, 2, 1, 0, 2, 1, 1, 0, 2, 2, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 1, 2, 2, 2, 0, 1, 1, 0, 0, 1, 2, 0, 0, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 0, 2, 0, 2, 1, 2, 0, 1, 2, 0, 1, 0, 1, 2, 0, 2, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 0, 0, 2, 1, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 2, 1, 0, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 2, 0, 2, 2, 1, 0, 0, 2, 1, 0, 1, 0, 2, 2, 0, 1, 1, 0, 2, 2, 1, 2, 1, 2, 1, 1, 1, 0, 0, 2, 0, 1, 2, 0, 0, 2, 0, 0, 0, 2]

max_len = len(g1) if len(g1) < len(g2) else len(g2)

for i in range(max_len):
    print(g1[i] == g2[i])
