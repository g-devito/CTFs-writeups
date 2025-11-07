#!/bin/python
flag_hex = '666c61677b68337834646563696d616c5f63346e5f62335f41424144424142457d'
flag_bin = bytes.fromhex(flag_hex)
flag_str = flag_bin.decode()

print(flag_str)
