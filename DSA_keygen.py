import time
import sys
import secrets
sys.setrecursionlimit(100000)


def lenght(x):

    count = 0

    if x == 0:
        return 1

    while x:
        count += 1
        x //= 10

    return count


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


def ciur():
    global erath
    global primes

    erath[0] = 1
    erath[1] = 1

    i = 2
    while i <= 500:
        if erath[i] == 0:

            j = i * i
            while j <= 250000:

                erath[j] = 1
                j += i

        i += 1

    for i in range(2, 250000):
        if erath[i] == 0:
            primes.append(i)


def bignumgen(b_dim):
    return secrets.randbits(b_dim)


def checkdiv(x):
    global primes

    for i in range(20000):
        if x % primes[i] == 0:
            return 0

    return 1


def primecheck(candidate):
    global primes

    if checkdiv(candidate) == 0:
        return False

    mod = candidate

    n_minus_1 = candidate - 1

    exp = 0

    while n_minus_1 & 1 == 0:
        n_minus_1 //= 2
        exp += 1

    dp = n_minus_1

    alist = primes[:15] + [primes[secrets.randbelow(22000) + 5] for i in range(35)]

    lalist = len(alist)

    for i in range(lalist):
        a = alist[i]

        ad = logpow(dp, a, mod)

        if ad != 1 and ad != candidate - 1:

            r_found = False

            for r in range(1, exp):

                ad *= ad
                ad %= candidate

                if ad == candidate - 1:
                    r_found = True

            if not r_found:
                return False

    return True


def primegen(b_dim):
    global primes

    candidate = bignumgen(b_dim)

    while not primecheck(candidate):
        candidate = bignumgen(b_dim)

    return candidate


# ----------------------------------- main ------------------------------------


print('initialization...')

t = time.time()

erath = [0 for i in range(250001)]
primes = []
ciur()
print('prime set initialized (', time.time() - t, ' seconds )')
print('\n')

ok = False

p = 0
q = 0

t = time.time()

while not ok:

    q = primegen(256)

    for _ in range(1000):

        aux_big_num = secrets.randbits(3072)

        p_candidate = aux_big_num - (aux_big_num % q) + 1

        if primecheck(p_candidate):

            p = p_candidate

            ok = True
            break

print('primes p and q generated (', time.time() - t, ' seconds )')
print('\n')

t = time.time()

g = 0

aux_exp = (p - 1) // q

ok = False

while not ok:

    aux_base = secrets.randbelow(p - 2) + 2

    g_candidate = logpow(aux_exp, aux_base, p)

    if g_candidate != 1:

        g = g_candidate

        ok = True

print('generator g of random subgroup of order q in (Z/pz)* generated (', time.time() - t, ' seconds )')
print('\n')

x = secrets.randbelow(q - 1) + 1
y = logpow(x, g, p)

pubk = open('DSA_public_key.txt', 'w')
privk = open('DSA_private_key.txt', 'w')

pubk.write(str(y))
pubk.write('\n')
pubk.write(str(p))
pubk.write('\n')
pubk.write(str(q))
pubk.write('\n')
pubk.write(str(g))

privk.write(str(x))

print('public key y generated ( found in file DSA_public_key.txt on line 0 ) ')
print('parameters p, q and g found in DSA_public_key.txt on lines 1, 2 and 3 in this order')
print('private key x generated (found in file DSA_private_key.txt on line 0 )')










