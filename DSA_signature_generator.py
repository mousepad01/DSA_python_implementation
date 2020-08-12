import time
import secrets
from hash_functions import sha256


def logpow(exp, base, mod):
    base %= mod

    if exp == 0:
        return 1

    if exp == 1:
        return base % mod

    if exp & 1 == 0:
        return logpow(exp // 2, base ** 2, mod) % mod

    if exp & 1 == 1:
        return (base * logpow(exp // 2, base ** 2, mod) % mod) % mod


def egcd(a, b):
    x = 0
    y = 1
    u = 1
    v = 0
    while a != 0:
        q = b // a
        r = b % a
        m = x - u * q
        n = y - v * q
        b = a
        a = r
        x = u
        y = v
        u = m
        v = n
    return x


def signature_generator(m):

    privk = open("DSA_private_key.txt")
    pubk = open("DSA_public_key.txt")

    auxy = pubk.readline()  # nu am nevoie dar il citesc

    auxp = pubk.readline()
    p = int(auxp[:len(auxp) - 1])

    auxq = pubk.readline()
    q = int(auxq[:len(auxq) - 1])

    auxg = pubk.readline()
    g = int(auxg[:len(auxg)])

    auxx = privk.readline()
    x = int(auxx[:len(auxx)])

    k = secrets.randbelow(q - 1) + 1

    r = logpow(k, g, p) % q

    while r == 0:
        r = logpow(k, g, p) % q

    inv_k = egcd(k, q)

    while inv_k < 0:
        inv_k += q

    s = (inv_k * (sha256(m) + x * r)) % q

    while s == 0:

        k = secrets.randbelow(q - 1) + 1

        r = logpow(k, g, p) % q

        while r == 0:
            r = logpow(k, g, p) % q

        inv_k = egcd(k, q)

        while inv_k < 0:
            inv_k += q

        s = (inv_k * (sha256(m) + x * r)) % q

    return r, s


