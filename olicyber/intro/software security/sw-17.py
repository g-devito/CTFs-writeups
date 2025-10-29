#!/usr/bin/env python3

# Importa la libreria di pwntools
from pwn import *
import ast


def main():
    HOST = "software-17.challs.olicyber.it"
    PORT = 13000
    r = remote(HOST, PORT)

    r.sendline(b"ciao")
    for _ in range(7):
        print(r.recvline())

    for i in range(10):
        # get bytes coded array
        nums = ast.literal_eval(r.recvline().decode())
        print(nums)
        
        # sum it and send back
        summed = str(sum(nums)).encode()
        print(summed)
        r.sendline(summed)

        for _ in range(2):
            print(r.recvline())

    r.close()

if __name__ == "__main__":
    main()
