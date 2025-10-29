#!/usr/bin/env python3

ciphertext = '104e137f425954137f74107f525511457f5468134d7f146c4c'

ciphertext_byte = bytes.fromhex(ciphertext)

for i in range(128):
    xored = bytes(byte ^ i for byte in ciphertext_byte)
    if all(32 <=x <= 126 for x in xored):
        print(xored.decode('ascii'))
