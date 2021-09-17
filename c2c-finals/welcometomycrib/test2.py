import binascii, sys, string

C1_hex = "62496295bb5561c82d7573671a4cc4bd6d4d7194bb4666db3a623d340c4dc3f16d086485e94f29c93a733a701a00c5ef6e5d7e94bb5566ca3a643b710d00cefc6f4f6591fc4429d937753d340f49c1e9745a75d0f84e65c97f7c36605f54c3f16a087891e8017edf366436341945c7e9214e7f85e9017ec53a6236341052c6f8730844a2ce6429da37753d340c45c3"
C2_hex = "734d7d95f6436cdf7f723f751c4b82fc6f4c3084fe527d8d3b65217d114782ee6051309efe576cdf7f643b661a4582ea64417798ef0160c32b7521710c5482ee714d7c9cbb4760c1333032731a00c5f47344309cf2527dc83130247c1643cabd6c477e95e20161c82d7573631a52c7bd725c7580bb4e67c126303e750d4b82f16e5f3092fe4668c37f63267a"

C1 = binascii.unhexlify(C1_hex)
C2 = binascii.unhexlify(C2_hex)


def xor(a, b):
    return bytes([x ^ y for x,y in zip(C1, C2)])

# print(binascii.hexlify(xor(C1, C2)))

P_xored = xor(C1, C2)[:16]

# print(P_xored.hex())

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
        smallest_len = len(p1_test)
        if len(p2_test) < smallest_len:
            smallest_len = len(p2_test)
        if xor_test[:smallest_len] == P_xor_test[:smallest_len] and not p1_test == p2_test:
            print("FOUND WORDS!")
            print("P1:", p1_test)
            print("P2:", p2_test)
            sys.exit(0)
