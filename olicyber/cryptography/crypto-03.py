#!/usr/bin/env python3

from base64 import b64decode
from math import ceil

half_flag_b64 = 'ZmxhZ3t3NDF0XzF0c19hbGxfYjE='
half_flag_b10 = 664813035583918006462745898431981286737635929725

flag_decoded = b64decode(half_flag_b64) + (half_flag_b10).to_bytes(ceil(half_flag_b10.bit_length() / 8), "big")

print(flag_decoded.decode())
