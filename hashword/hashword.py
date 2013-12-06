#!/usr/bin/env python

from hashlib import sha256
import random
import subprocess
import argparse


def hashword(pw, length=16, seed=1, no_spec_chars=False):
    """
    Returns an new password using `pw`, hexdigest of sha256

    pw              - can be the name of the login, for instance
    length          - how many characters the password will be, default 16
    seed            - for PRNG (this is your key), default 1
    no_spec_chars:
        False = Letters and Numbers only
        True  = Letters, Numbers, and Special Characters
    If you're okay with 16-character passwords, you can use a length
    of type(str) and get some unique seed values for the PRNG.
    """

    DEFAULT_LENGTH, MINIMUM_LENGTH = 16, 8

    #use `length` of type(str) and get some unique seed values for the PRNG.
    seed = str(seed) + str(length)

    try:
        length = int(length)
    except (ValueError, TypeError):
        length = DEFAULT_LENGTH

    try:
        pw = str(pw)
    except (ValueError, TypeError):
        raise TypeError('Passwords must have legal str() form')

    if length < 8:
        length = MINIMUM_LENGTH

    # for arbitrarily long password output, change the length of the constants
    len_mod = (length + 33) / 32 + 1

    pw_list = list(sha256(pw + str(length)).hexdigest())
    len_pw = len(pw_list)
    while len_pw < length:
        pw_list += pw_list
        len_pw *= 2

    SPEC = '~!@#$%^&*()-_=+{}:",./?!@+' * len_mod
    LOWR = 'abcdefghijklmnopqrstuvwxyz' * len_mod
    UPPR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' * len_mod
    NUMS = '01234567890123456789012345' * len_mod
    # for the sha-256
    HNUMS = '0123456789abcdef'

    # shuffle the constants, using `seed`
    SPEC = ''.join(seedsort(SPEC, seed))
    LOWR = ''.join(seedsort(LOWR, seed))
    UPPR = ''.join(seedsort(UPPR, seed))
    NUMS = ''.join(seedsort(NUMS, seed))

    # set the charsets into a tuple (for round-robin selection)
    if no_spec_chars:
        used = UPPR, LOWR, NUMS
    else:
        used = SPEC, UPPR, LOWR, NUMS

    # randrange up to half the len to avoid index errors
    seeded = [random.randrange(0, len_pw / 2) for i in range(len_pw)]

    charsets = len(used)
    for idx, i in enumerate(pw_list):
        # idx % charsets iterates through the available character sets
        # round-robin style, ensuring even distribution of alphanums/specials
        pw_list[idx] = used[idx % charsets][seeded[idx] + HNUMS.index(i)]

    pw_list = seedsort(pw_list[:length], seed)
    return ''.join(pw_list)


def seedsort(iterable, seed):
    """return shuffle of `iterable` from random.seed(`seed`) as a list"""
    random.seed(str(seed) + str(iterable[-1]))
    return [ix[1] for ix in sorted((random.random(), i) for i in iterable)]


def clipboard(word):
    """Linux only, for now: xsel is required"""
    # primary
    xsel_proc = subprocess.Popen(['xsel', '-pi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(word)
    # clipboard
    xsel_proc = subprocess.Popen(['xsel', '-bi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(word)
    # TODO: Windows, POSIX


def sample(n):
    """analyze the results of hashword to `n` loops"""
    from pprint import pprint
    results = {}
    pw = hashword('droogans@gmail.com', n, n)
    types = {'isupper': 0, 'islower': 0, 'isdigit': 0, 'spec': 0}
    for i in pw:
        results[pw] = types
        if i.isdigit():
            results[pw]['isdigit'] += 1
        elif i.islower():
            results[pw]['islower'] += 1
        elif i.isupper():
            results[pw]['isupper'] += 1
        else:
            results[pw]['spec'] += 1
    pprint(results)


if __name__ == '__main__':
    #cli
    desc = 'Enchances password, copies directly to clipboard.'
    epil = 'email issues to: droogans@gmail.com'
    parser = argparse.ArgumentParser(description=desc, epilog=epil)
    parser.add_argument('pw', type=str,
                        help='original password')
    parser.add_argument('-l', dest='length',
                        required=False, type=int, default=16,
                        help='desired length of new password')
    parser.add_argument('-k', dest='seed', required=False, type=str, default=1,
                        help='secret key for PRNG')
    parser.add_argument('-s', dest='no_spec_chars', action='store_true',
                        default=False, help='if set, use only [a-zA-Z0-9]')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1',
                        help='print the module and version, then quit')
    args = vars(parser.parse_args())
    clipboard(hashword(**args))
