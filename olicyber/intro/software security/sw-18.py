#!/usr/bin/env python3

from pwn import *
import ast

def main():
    HOST = "software-18.challs.olicyber.it"
    PORT = 13001
    r = remote(HOST, PORT)

    r.sendline(b"ciao")
    for _ in range(7):
        r.recvline()

    for i in range(100):
        line = r.recvline()

        m = re.search(rb'0x[0-9a-fA-F]+', line)
        number = int(m.group(0), 0) if m else (print(line, i) or None)

        packed_num = p32(number) if '32-bit' in line.decode() else p64(number)
        r.send(packed_num)
        packed_num

        r.recvline()

    print(r.recvline())

    r.close()

if __name__ == "__main__":
    main()
