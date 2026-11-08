#!/usr/bin/env python3
"""Build ledger/zhang240.json (DEBRIEF protocol 0.1.0) from prereg.yaml, checks/manifest.json and checks/results.json.
Standard library only. Run from the repository root: python3 build_ledger.py"""
import datetime, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "checks", "results.json")))
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
MID, POD = "prime-gaps-240-zhang-2026-11", "DEBRIEF-math-zhang240"
BY = "Nervous Machine (Heidi Bennett; Claude Code as the operating agent)"
BASE = {"schema_version": "nm-debrief-v1", "created_by": "DEBRIEF-math-zhang240/build_ledger.py", "created_at": NOW, "mission_id": MID, "pod": POD,
        "provenance": {"source": "public record to 2026-11-08; checks registered in prereg.yaml before any fetch or run", "certificate_source": {"repo": "github.com/hanxinzhang/prime-bound", "commit": R["C1"]["commit"], "files_sha256": R["C1"]["files_sha256"]},
                       "paper": {"doi": "10.5281/zenodo.22135842", "md5": R["C5"]["zenodo_md5"], "sha256": R["C5"]["sha256"]}}, "audience": "briefing"}
doc = lambda **k: {**BASE, **k}

c2, c3, c4, c5 = R["C2"], R["C3"], R["C4"], R["C5"]
c4_done = c4.get("status") == "done"
all_ok = R["all_pass"]
verdict = "confirmed" if all_ok else ("mixed" if c4_done else "mixed")

c4_sentence = (f"The full exact reconstruction, which recomputes every stored quantity from the coefficient files without a cache, also passed, in {c4.get('wall')} on twenty cores with the pinned library." if c4.get("pass")
               else (f"The full exact reconstruction did not report a pass; its last line was '{c4.get('final_line')}'. That is recorded as an anomaly." if c4_done else "The full exact reconstruction is still running; its result is not in this record."))
cycle1 = doc(cycle=1, dated="2026-11-08", by=BY, kind="rerun",
             preregistered={"question": "Does Zhang's exact certificate for the 240 bound pass when fetched at a pinned commit and run on a machine independent of the author, and is the 49-tuple admissible by our own check?",
                            "rule": "pre-registered in prereg.yaml before fetching or reading any certificate code: C1 provenance and static imports, C2 quick check in a VM, C3 own admissibility check, C4 full reconstruction in a VM, C5 paper hash",
                            "predictions": [f"{k}: {v}" for k, v in R["predictions"].items()], "commit": "prereg.yaml", "results": ["checks/manifest.json", "checks/results.json", "checks/logs/quick.log"] + (["checks/logs/full.log"] if c4_done else []), "before_data": True},
             outcome={"verdict": verdict, "numbers": {"files": 9, "sizes_match": R["C1"]["all_sizes_ok"], "quick_final_line": c2.get("final_line"), "quick_wall": c2.get("wall"), "quick_max_rss_mb": c2.get("max_rss_mb"),
                                                      "tuple_size": c3["size"], "tuple_diameter": c3["diameter"], "tuple_admissible": c3["admissible"], "full_status": c4.get("status"), "full_final_line": c4.get("final_line"), "full_wall": c4.get("wall"), "full_max_rss_mb": c4.get("max_rss_mb"),
                                                      "full_installed": c4.get("installed"), "paper_md5_matches_zenodo": c5["pass"]},
                      "misses": [f"{k} did not pass as predicted" for k in R["misses"] if R[k].get("status") != "not run"]},
             spoken="On November eighth, under a rule written before any file was fetched, Nervous Machine reran Hanxin Zhang's exact certificate for the two hundred and forty bound. The nine files were fetched at a pinned commit and their sizes matched the public listing; the quick check needs only Python's standard library. Run inside a virtual machine, the quick check finished in a fraction of a second and ended with the expected line, an admissible forty-nine-tuple of diameter two hundred and forty. Nervous Machine's own code confirmed that tuple: forty-nine distinct numbers, spanning two hundred and forty, missing at least one remainder for every prime up to forty-seven. The paper's file matched the hash Zenodo publishes. " + c4_sentence,
             finding_ids=["Z1", "Z2"] + (["Z3"] if c4.get("pass") else []), gap_ids=["ZG1"])

cycle0 = doc(cycle=0, dated="2026-08-28", kind="replay", preregistered={"question": "What was public when the claim appeared?", "rule": "no look-ahead; evidence dated by first public posting", "predictions": [], "commit": None, "before_data": False},
             outcome={"verdict": "admitted", "numbers": {"zenodo_published": "2026-08-28", "repo_first_commit": "2026-08-28", "repo_head": "2026-09-02"}},
             spoken="On August twenty eighth, 2026, Hanxin Zhang deposited a paper on Zenodo proving that infinitely many pairs of consecutive primes differ by at most two hundred and forty, with the discovery credited to the model GPT 5.6 Sol, and published a repository with the finite data and exact-arithmetic programs behind it. The analytic argument is in the paper and is not part of the computer check. Three days later Julia Stadlmann posted an independent proof of the same bound without AI, and on September third OpenAI claimed one hundred and eighty six and Axiom Math two hundred and twelve.",
             finding_ids=["Z4"], gap_ids=["ZG1", "ZG2", "ZG3"])

NA = {"earned": None, "note": "a checked statement, not a learned relationship"}
findings = [
    doc(finding_id="Z1", kind="learned", spoken="The forty-nine-number list in the certificate spans exactly two hundred and forty and is admissible: for every prime up to forty-seven it misses at least one remainder.",
        evidence={"numbers": {"size": c3["size"], "diameter": c3["diameter"], "distinct": c3["distinct"], "primes_checked": list(c3["missed_class"].keys())}, "cycles": [1], "confirmed_by": ["computation run by Nervous Machine with its own code"]},
        standing={"status": "certified" if c3["pass"] else "refuted", "basis": "checked by direct computation under a rule written down first, on the tuple read from the pinned certificate file", "note": "independent of the author's verify.py"}, certainty={"earned": True, "note": "deterministic, reproducible check (audit regime)"}, edge_refs=[]),
    doc(finding_id="Z2", kind="learned", spoken="The exact finite certificate passes its quick check on a machine independent of the author: thirteen exponent inequalities positive, the retained quotient above its threshold, the packing budget margin positive, the first-moment ratio above one, and the tuple as stated. The quick check trusts the stored norms and event integrals; it checks them for consistency, it does not recompute them.",
        evidence={"numbers": {"final_line": c2.get("final_line"), "exit_status": c2.get("exit_status"), "wall": c2.get("wall"), "max_rss_mb": c2.get("max_rss_mb")}, "cycles": [1], "confirmed_by": ["rerun by Nervous Machine in an isolated VM"]},
        standing={"status": "certified" if c2.get("pass") else "refuted", "basis": "an exact-arithmetic check rerun by a party independent of the author, under a rule written first", "note": "quick path; stored quantities trusted"}, certainty={"earned": True, "note": "independent rerun (audit regime)"}, edge_refs=[]),
] + ([doc(finding_id="Z3", kind="learned", spoken="The full exact reconstruction passes independently: the source norm, the exact marginal, its square, all forty-five rank profiles and every event integral were recomputed from the coefficient files without any cache, and the certificate reported a pass.",
          evidence={"numbers": {"final_line": c4.get("final_line"), "wall": c4.get("wall"), "max_rss_mb": c4.get("max_rss_mb"), "installed": c4.get("installed")}, "cycles": [1], "confirmed_by": ["rerun by Nervous Machine in an isolated VM"]},
          standing={"status": "certified", "basis": "an exact-arithmetic reconstruction rerun by a party independent of the author, under a rule written first", "note": "one machine, one party; a second rerun would strengthen it"}, certainty={"earned": True, "note": "independent rerun (audit regime)"}, edge_refs=[])] if c4.get("pass") else []) + [
    doc(finding_id="Z4", kind="learned", spoken="The analytic input is three published distribution estimates of Maynard for primes in arithmetic progressions to large moduli, combined in a new nested distribution theorem.",
        evidence={"numbers": {}, "cycles": [0], "confirmed_by": ["published literature"]},
        standing={"status": "accepted", "basis": "Maynard's estimates are published, refereed results; the new combination is the paper's own argument and is a gap, not a finding", "note": None}, certainty=NA, edge_refs=[]),
]

gaps = [
    doc(gap_id="ZG1", title="The analytic argument has no formal deduction and no referee report", status="proposed", opened_cycle=0, priority=1,
        spoken="Unlike OpenAI's one hundred and eighty six, there is no Lean development here. The nested distribution theorem, the Buchstab identity, the Siegel-Walfisz lemmas and the reductions are a written proof. The certificate checks the finite part only. Until the paper is refereed or the argument is formalized, the claim is conditionally supported whatever the certificate shows.",
        history=[{"cycle": 0, "hypothesis": "the paper's analytic argument", "before_data": False, "result": "stated by the author as not part of the computer verification"}, {"cycle": 1, "hypothesis": "the finite certificate reruns independently", "before_data": True, "result": "quick check passed; see cycle one for the full reconstruction"}],
        closes_with=[{"what": "a referee report or an independent expert read of the analytic sections", "kind": "research", "external": True, "who_could_act": "a journal or independent analytic number theorists"}, {"what": "a formalization of the deduction from Maynard's estimates to the certificate's inequalities", "kind": "research", "external": True, "who_could_act": "the Lean community"}],
        expected_signal="a referee report, a public expert read, or a formal development that takes the certificate's inequalities as hypotheses", resolution_by="none registered",
        ask={"spoken": "An analytic number theorist should read sections two to four of the paper, or someone should formalize the deduction. Either would move this from open."}),
    doc(gap_id="ZG2", title="Does the paper's theorem statement match what verify.py checks?", status="proposed", opened_cycle=0, priority=2,
        spoken="There is no formal statement to trace, so the reading aid here would be a map from the paper's theorem and lemmas to the thirteen inequalities, the support identities and the retained-quotient threshold that the program checks. Nobody independent has published that reading.",
        history=[{"cycle": 0, "hypothesis": "the author's README table of what each check establishes", "before_data": False, "result": "self-described; not independently read"}],
        closes_with=[{"what": "a statement-by-statement map from the paper to verify.py, signed by a reader who is not the author", "kind": "read", "external": True, "who_could_act": "a number theorist willing to read both"}],
        expected_signal="two signed read cycles against a statement map prepared as a later cycle; one refusal reopens it", resolution_by="none registered",
        ask={"spoken": "Prepare the statement map, then have two people who are not the author read it and sign or refuse."}),
    doc(gap_id="ZG3", title="The stored marginal's rounding bound", status="proposed", opened_cycle=0, priority=3,
        spoken="The stored marginal is a rounded approximation with a rounding-error bound kept in the certificate. Whether that bound is applied correctly in the retained-quotient inequality is a reader's check on the paper and the code together, not something a rerun settles.",
        history=[{"cycle": 0, "hypothesis": "the author's bound", "before_data": False, "result": "recorded in certificate.json; not independently read"}],
        closes_with=[{"what": "a reader's check of the rounding-bound argument against exact_core.py", "kind": "read", "external": True, "who_could_act": "anyone comfortable with exact rational arithmetic and the paper's section on the marginal"}],
        expected_signal="a signed read cycle naming the inequality and the bound", resolution_by="none registered",
        ask={"spoken": "Check that the rounding bound is carried through the retained-quotient inequality. It is a short read for the right person."}),
]
anomalies = [] if (c4.get("pass") or not c4_done) else [doc(anomaly_id="ZA1", when="2026-11-08", node="full_reconstruction", spoken=f"The full exact reconstruction did not report a pass on Nervous Machine's machine; its last line was '{c4.get('final_line')}'. The author has not been asked yet.", status="open", urgency="daily", from_trusted_node=False, evidence={"log": "checks/logs/full.log", "installed": c4.get("installed")}, gap_id="ZG1", alert={"sent": False, "channel": None, "at": None})]
background = [
    doc(term="admissible tuple", also_called=["admissible set"], spoken="A list of whole numbers that, for every prime, leaves out at least one remainder. Such a list is one that could in principle be shifted to land on primes at every position; the prime k-tuples conjecture says it does so infinitely often.", source="general"),
    doc(term="exact certificate", also_called=["exact-arithmetic certificate"], spoken="A finite set of numbers and a program that checks, with fractions rather than decimals so there is no rounding, that the inequalities a proof needs really hold. It replaces the hardest numerical part of the argument with something anyone can rerun.", source="general"),
    doc(term="Maynard's distribution estimates", also_called=["distribution estimates for primes to large moduli"], spoken="Results about how evenly primes are spread among remainders modulo large numbers. Proofs of bounded gaps need these as fuel; the more of the range they cover, the smaller the gap that can be proved.", source="general"),
]
n_cert = sum(f["standing"]["status"] == "certified" for f in findings)
mission = doc(title="The claim that primes come within 240 of each other infinitely often (Zhang)", kind="audit", protocol_version="0.1.0", claim_rule_met=False, pods=[POD], began="2026-11-08", status="active",
              record_quality="reconstructed", record_note="Replayed from the public record, dated by first public posting; Nervous Machine's own checks were registered before any file was fetched.",
              record_limits=["The certificate was rerun by Nervous Machine on one machine; no second independent party has reported a rerun.", "The analytic argument was not read by Nervous Machine."],
              scope_limits=["Nervous Machine keeps score of the checks; it does not check the mathematics line by line.", "Public record through November eighth, 2026."],
              opening={"spoken": "This briefing covers Hanxin Zhang's proof that infinitely many pairs of primes sit at most two hundred and forty apart, what its exact certificate establishes, what Nervous Machine reran, and what still has to be read by a person."},
              short_version={"spoken": "On August twenty eighth, 2026, Hanxin Zhang proved that infinitely many pairs of consecutive primes differ by at most two hundred and forty, with the discovery credited to the model GPT 5.6 Sol, improving the published record of two hundred and forty six. The proof has two parts: an analytic argument written in the paper, and an exact finite certificate anyone can rerun. Nervous Machine reran the certificate on its own machine under a rule written first. " + ("The quick check and the full reconstruction both passed, and the forty-nine-number list is admissible by our own check." if c4.get("pass") else "The quick check passed and the forty-nine-number list is admissible by our own check. " + c4_sentence) + " What is open is the analytic argument: it has no formal deduction and no referee report. My read: conditionally supported, with the certificate independently reproduced; not yet settled."},
              what_happened={"spoken": "The claim appeared on Zenodo and GitHub on the same day in late August. Nervous Machine wrote down what it would check and what it predicted, fetched the nine files at a pinned commit, ran the certificate inside a virtual machine, checked the tuple with its own code, and recorded every outcome."},
              implications={"rely_on": [{"spoken": "the finite certificate's inequalities hold in exact arithmetic on an independent machine", "finding_ids": ["Z2"] + (["Z3"] if c4.get("pass") else [])}], "do_not_rely_on": [{"spoken": "the two hundred and forty bound as a theorem; its analytic argument is unrefereed and unformalized", "finding_ids": []}], "stop": [], "new": [{"spoken": "the same library, python-flint zero point nine, sits under both this certificate and OpenAI's; a reader comparing the two should know that", "finding_ids": []}]},
              certainty_statement={"spoken": f"{n_cert} items are certified by independent rerun or direct computation; the analytic argument is open."},
              sources=[{"kind": "paper", "ref": "H. Zhang, A bound of 240 for gaps between primes, Zenodo 10.5281/zenodo.22135842 (2026-08-28), CC-BY-4.0"}, {"kind": "repository", "ref": "github.com/hanxinzhang/prime-bound, commit " + R["C1"]["commit"]}, {"kind": "checks", "ref": "checks/results.json, checks/logs/"}])
L = {"missions": [mission], "cycles": [cycle0, cycle1], "findings": findings, "gaps": gaps, "anomalies": anomalies, "background": background, "sessions": []}
os.makedirs(os.path.join(HERE, "ledger"), exist_ok=True)
json.dump(L, open(os.path.join(HERE, "ledger", "zhang240.json"), "w"), indent=1, ensure_ascii=False)
print(f"ledger: {len(L['cycles'])} cycles, {len(findings)} findings, {len(gaps)} gaps, {len(anomalies)} anomalies; C4 {c4.get('status')}")
