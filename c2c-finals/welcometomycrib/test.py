import binascii, sys

C1_hex = "0c2c0e052b1a01"
C2_hex = "19231a1a35061b26"

C1 = binascii.unhexlify(C1_hex)
C2 = binascii.unhexlify(C2_hex)

print(C1)
print(C2)

def xor(a, b):
    return bytes([x ^ y for x,y in zip(C1, C2)])

print(binascii.hexlify(xor(C1, C2)))

P_xored = xor(C1, C2)

print(P_xored)

with open("smaller_english.txt", "r") as f:
    wordlist = f.readlines()
    wordlist = [w[:-1] for w in wordlist]


# print(wordlist)

p1_known = []
p2_known = []

for p1_word_test in wordlist:
    p1_test = " ".join(p1_known + [p1_word_test])
    for p2_word_test in wordlist:
        p2_test = " ".join(p2_known + [p2_word_test])
        xor_test = xor(p1_test.encode(), p2_test.encode())
        P_xor_test = P_xored[:len(xor_test)]
        if xor_test == P_xor_test:
            print("FOUND WORDS!")
            print("P1:", p1_test)
            print("P2:", p2_test)
            sys.exit(0)
