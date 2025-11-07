#!/usr/bin/env python3
from pwn import *

exe = ELF("sw-19")

p = remote("software-19.challs.olicyber.it", 13002)

# read banner
for _ in range(7):
    print(p.recvline())
print(p.recv(49))
p.sendline(b'1')

for _ in range(20):
    # get function name & mem address
    fun_name = p.recvuntil(b": ").split()[1][:-1]
    mem_addr = hex(exe.sym[fun_name]).encode()
    print(fun_name, ": ", mem_addr)

    # send mem address
    p.sendline(mem_addr)

flag = p.recvline().split()[-1].decode()
print(flag)

p.close()
