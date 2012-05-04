Hashword 
========
usage: hashword.py [-h] [-l L] [-k K] [-s] password

Enchances password, copies directly to clipboard.

positional arguments:
  password    original password

optional arguments:
  -h, --help  show this help message and exit
  -l L        desired length of new password
  -k K        secret key for PRNG
  -s          if set, use only [a-zA-Z0-9]

email issues to: droogans@gmail.com

Requirements
============
Python 2.7

xsel

Suggested usage
===============
    >$ python -m hashword login@service.tld -l 64 -k b4d_pa$$w0rd
    >$ google-chrome https://www.grc.com/haystack.htm

Changelog
=========
20120409 v0.1 - Created project 

Notes
=====
Just because this script makes it much easier to generate very strong
passwords doesn't mean you shouldn't take the extra effort to further
strengthen your set of passwords. Use the flags provided to do this.

Always use the -l modifier to something other than 16. You can go as low
as eight characters, but it is *strongly* recommended that you go as 
high as 64 characters. Choosing odd numbers (say, primes) is likely to 
be easier to remember (the only prime numbers in the 30's is 31 and 37),
making it that less likely to be exploited should an attacker realize
you're using this program to generate passwords. It is also strongly 
recommended that you always use the -k flag to define your own key for
shuffling the results of your final password.

The -s flag is included for situations where only alphanumeric 
characters are allowed by the service accepting your password.

Help
====
email issues to droogans@gmail.com
