# Asks — The claim that primes come within 240 of each other infinitely often (Zhang)

Each open gap below is a place a contribution can land. A contribution is one cycle in this repository's ledger, under your name. How to contribute, and the templates: https://github.com/Nervous-Machine/DEBRIEF/blob/main/CONTRIBUTING.md

## 1. The analytic argument has no formal deduction and no referee report (ledger id ZG1)

Unlike OpenAI's one hundred and eighty six, there is no Lean development here. The nested distribution theorem, the Buchstab identity, the Siegel-Walfisz lemmas and the reductions are a written proof. The certificate checks the finite part only. Until the paper is refereed or the argument is formalized, the claim is conditionally supported whatever the certificate shows.

Status: proposed.

- **a referee report or an independent expert read of the analytic sections** — contribution kind: claim or research; who could act: a journal or independent analytic number theorists.
- **a formalization of the deduction from Maynard's estimates to the certificate's inequalities** — contribution kind: claim or research; who could act: the Lean community.

Signal expected: a referee report, a public expert read, or a formal development that takes the certificate's inequalities as hypotheses. Resolution by: none registered.

## 2. Does the paper's theorem statement match what verify.py checks? (ledger id ZG2)

There is no formal statement to trace, so the reading aid here would be a map from the paper's theorem and lemmas to the thirteen inequalities, the support identities and the retained-quotient threshold that the program checks. Nobody independent has published that reading.

Status: proposed.

- **a statement-by-statement map from the paper to verify.py, signed by a reader who is not the author** — contribution kind: read; who could act: a number theorist willing to read both.

Signal expected: two signed read cycles against a statement map prepared as a later cycle; one refusal reopens it. Resolution by: none registered.

## 3. The stored marginal's rounding bound (ledger id ZG3)

The stored marginal is a rounded approximation with a rounding-error bound kept in the certificate. Whether that bound is applied correctly in the retained-quotient inequality is a reader's check on the paper and the code together, not something a rerun settles.

Status: proposed.

- **a reader's check of the rounding-bound argument against exact_core.py** — contribution kind: read; who could act: anyone comfortable with exact rational arithmetic and the paper's section on the marginal.

Signal expected: a signed read cycle naming the inequality and the bound. Resolution by: none registered.
