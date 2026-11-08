# DEBRIEF-math-zhang240

A DEBRIEF mission record (protocol https://github.com/Nervous-Machine/DEBRIEF): a pre-registered, independent rerun
of Hanxin Zhang's exact certificate for the claim that infinitely many pairs of consecutive primes differ by at
most 240 (paper: Zenodo 10.5281/zenodo.22135842, 28 August 2026, discovery credited to GPT 5.6 Sol; certificate:
github.com/hanxinzhang/prime-bound). The ledger is `ledger/zhang240.json`.

**Standing.** See `SCORECARD.md`, rendered from the ledger. The claim is conditionally supported: the finite
certificate reproduces on an independent machine, and the analytic argument has neither a formal deduction nor a
referee report. This record does not call the bound a theorem.

## What was done, in order

1. **Pre-registration** (`prereg.yaml`, hashed in `prereg.yaml.sha256` at 20:27 UTC on 8 November 2026) written
   before any certificate file was fetched and before any of its code was read. It names the commit, the files
   and their sizes from the GitHub API, the steps of the claim, five checks and a predicted outcome for each.
2. **C1, provenance.** The nine files were fetched at commit `2319570b` into an isolated directory; sizes matched;
   sha256 for each is in `checks/manifest.json`. By static inspection the quick check imports only the Python
   standard library; the full reconstruction needs `python-flint==0.9.0`, the same library OpenAI's 186 certificate
   uses.
3. **C2, quick check**, run inside a virtual machine, never on the host: `python3 -B -I -S verify.py` ended with
   `admissible 49-tuple diameter: 240`, exit 0. Log: `checks/logs/quick.log`.
4. **C3, our own tuple check.** `checks/admissible.py` (written for this mission) read the 49-tuple from the
   certificate file: 49 distinct integers, diameter 240, a missed residue class for every prime up to 47.
5. **C4, full exact reconstruction**, `verify.py --full` in a fresh virtual environment inside the VM. Its outcome
   is in `checks/results.json` and `checks/logs/full.log` when complete; the ledger says "running" until then.
6. **C5, paper.** The PDF's md5 matches the hash Zenodo publishes.

Predictions and outcomes are compared in `checks/results.json`; misses, if any, are listed there and in the cycle.

## Why nothing from the certificate repository is copied here

The repository states no licence. This record keeps its commit id, each file's sha256 and a fetch script
(`checks/fetch.py`). The paper is CC-BY-4.0.

## What remains open

In `ASKS.md`, in order: the analytic argument (a referee or an expert read, or a formalization); a statement map
from the paper's theorem to what `verify.py` checks, signed by readers who are not the author; the rounding bound
on the stored marginal, a short read for the right person. Each is a place a contribution can land, as a dated
cycle under the contributor's name (https://github.com/Nervous-Machine/DEBRIEF/blob/main/CONTRIBUTING.md).

## Layout

```
prereg.yaml, prereg.yaml.sha256   the pre-registration and its hash
checks/fetch.py                   C1: fetch at the pinned commit, record hashes and imports
checks/manifest.json              C1 output
checks/admissible.py              C3: Nervous Machine's own admissibility check
checks/tuple_from_certificate.json
checks/run_vm.sh                  C2 and C4 inside the Lima VM
checks/logs/                      quick.log, full.log (GNU time output included)
checks/collect.py -> checks/results.json
build_ledger.py -> ledger/zhang240.json
SCORECARD.md, ASKS.md             rendered from the ledger
cycles/                           contributed cycles
```
