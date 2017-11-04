from __future__ import print_function, unicode_literals
from os import urandom
import re
from itertools import product
from functools import reduce
from operator import add

lower_case = 'abcdefghijklmnopqrstuvwxyz'
Passwords = product([x for x in lower_case], repeat=3)


def xor_decrypt():
    with open('Message', 'r') as file:
        msg = list(map(lambda x: int(x), re.split(",", file.readline())))
    return msg


def find_password():
    encyrpted = xor_decrypt()
    Message_Len = len(encyrpted)
    count = 0
    with open('decodedMessage', 'w') as output:
        try:
            while True:
                count += 1
                threechars = Passwords.__next__()
                password = ''.join(threechars)
                repeatedpasskey = password
                while len(repeatedpasskey) < Message_Len:
                    repeatedpasskey = repeatedpasskey.__add__(password)
                message = xor_strings(encyrpted, [ord(x) for x in repeatedpasskey])
                filtered_message = list(filter(lambda x: x > 122 or x < 65, message))
                if len(filtered_message) < 300:
                    message = reduce(add, list(map(lambda x: chr(x), message)))
                    total = sum([ord(x) for x in message])
                    print(total, message)
        except StopIteration:
            return 'Finished Decryption'


def genkey(length):
    """Generate key"""
    return urandom(length)


def xor_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        # Text strings contain single characters
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))
    else:
        # Python 3 bytes objects contain integer values in the range 0-255
        return [a ^ b for a, b in zip(s, t)]


find_password()
