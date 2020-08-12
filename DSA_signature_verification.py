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


def verify_signature(r, s, m):

    pubk = open("DSA_public_key.txt")

    auxy = pubk.readline()
    y = int(auxy[:len(auxy) - 1])

    auxp = pubk.readline()
    p = int(auxp[:len(auxp) - 1])

    auxq = pubk.readline()
    q = int(auxq[:len(auxq) - 1])

    auxg = pubk.readline()
    g = int(auxg[:len(auxg)])

    if r <= 0 or s <= 0 or r >= q or s >= q:
        return False

    inv_s = egcd(s, q)

    while inv_s < 0:
        inv_s += q

    exp_g = (inv_s * sha256(m)) % q
    exp_y = (inv_s * r) % q

    if r % p != ((logpow(exp_g, g, p) * logpow(exp_y, y, p)) % p) % q:
        return False

    return True



