#!/usr/bin/env python3
"""C3: Nervous Machine's own admissibility check, written for this mission before the tuple was read.
usage: admissible.py TUPLE_JSON  (a JSON list of integers)  -> prints a JSON result; exit 0 iff pass.
Admissible: for every prime p <= len(tuple) (primes above the length are automatic) the residues mod p miss a class."""
import json, sys


def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def check(t):
    t = [int(x) for x in t]
    res = {"size": len(t), "distinct": len(set(t)) == len(t), "diameter": max(t) - min(t), "missed_class": {}}
    for p in primes_upto(len(t)):
        res["missed_class"][p] = len({x % p for x in t}) < p
    res["admissible"] = res["distinct"] and all(res["missed_class"].values())
    res["pass"] = res["admissible"] and res["size"] == 49 and res["diameter"] == 240
    return res


if __name__ == "__main__":
    r = check(json.load(open(sys.argv[1])))
    print(json.dumps(r, indent=1)); sys.exit(0 if r["pass"] else 1)
