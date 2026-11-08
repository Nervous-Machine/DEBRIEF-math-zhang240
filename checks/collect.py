#!/usr/bin/env python3
"""Collect C1-C5 outcomes into checks/results.json from the manifest, the VM logs, the tuple check and the paper
hashes. Reads only files this mission wrote. usage: collect.py [--pdf-md5 MD5 --pdf-sha256 SHA --pdf-bytes N]"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRED = {"C1": "pass; stdlib only", "C2": "pass", "C3": "pass", "C4": "pass; wall time unknown, predicted under four hours on 20 cores", "C5": "pass"}
ZENODO_MD5 = "c0ce97edf07ce1a10ca981e32c73677b"


def parse_log(path, final_expected):
    if not os.path.exists(path):
        return {"status": "not run"}
    text = open(path, errors="replace").read()
    lines = [l for l in text.splitlines() if l.strip()]
    prog = [l for l in lines if not l.startswith("\t") and not l.startswith("Command being timed")]
    m_exit = re.search(r"Exit status: (\d+)", text); m_wall = re.search(r"Elapsed \(wall clock\) time.*?: ([\d:.]+)", text); m_rss = re.search(r"Maximum resident set size \(kbytes\): (\d+)", text)
    final = prog[-1].strip() if prog else ""
    freeze = [l for l in lines if re.match(r"^[A-Za-z0-9_.-]+==", l)]
    if not m_exit:
        return {"status": "running", "last_line": final, "log": os.path.relpath(path, HERE)}
    return {"status": "done", "final_line": final, "final_line_matches": final == final_expected, "exit_status": int(m_exit.group(1)) if m_exit else None,
            "wall": m_wall.group(1) if m_wall else None, "max_rss_mb": round(int(m_rss.group(1)) / 1024, 1) if m_rss else None, "installed": freeze,
            "pass": bool(m_exit and m_exit.group(1) == "0" and final == final_expected), "log": os.path.relpath(path, HERE)}


def main(argv):
    opts = dict(zip(argv[::2], argv[1::2]))
    man = json.load(open(os.path.join(HERE, "manifest.json")))
    quick_imports_ok = man["imports"]["verify.py"]["non_stdlib"] == []
    c1 = {"pass": man["all_sizes_ok"] and quick_imports_ok, "all_sizes_ok": man["all_sizes_ok"], "quick_path_non_stdlib_imports": man["imports"]["verify.py"]["non_stdlib"],
          "full_path_non_stdlib_imports": sorted(set(man["imports"]["src/exact_core.py"]["non_stdlib"] + man["imports"]["src/full_verify.py"]["non_stdlib"])), "requirements_full": man["requirements_full"],
          "commit": man["commit"], "files_sha256": {k: v["sha256"] for k, v in man["files"].items()}}
    c2 = parse_log(os.path.join(HERE, "logs", "quick.log"), "admissible 49-tuple diameter: 240")
    tup = json.load(open(os.path.join(HERE, "tuple_from_certificate.json")))
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "admissible.py"), os.path.join(HERE, "tuple_from_certificate.json")], capture_output=True, text=True)
    c3 = {**json.loads(r.stdout), "tuple": tup, "source": "data/certificate.json admissible_tuple.tuple at the pinned commit", "checker": "checks/admissible.py (Nervous Machine's own code)"}
    c4 = parse_log(os.path.join(HERE, "logs", "full.log"), "full exact reconstruction: PASS")
    c5 = {"zenodo_md5": ZENODO_MD5, "observed_md5": opts.get("--pdf-md5"), "sha256": opts.get("--pdf-sha256"), "bytes": int(opts["--pdf-bytes"]) if "--pdf-bytes" in opts else None}
    c5["pass"] = c5["observed_md5"] == ZENODO_MD5
    out = {"prereg": "prereg.yaml (sha256 in prereg.yaml.sha256, registered 2026-11-08T20:27:16Z)", "predictions": PRED, "C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5,
           "environment": {"vm": "Lima 'primegaps', aarch64, 20 cores, 98 GB, Ubuntu, CPython 3.14.4 (quick) / venv with requirements-full.txt (full)", "host_execution_of_downloaded_code": False}}
    out["all_pass"] = all(out[k].get("pass") for k in ("C1", "C2", "C3", "C4", "C5"))
    out["misses"] = [k for k in ("C1", "C2", "C3", "C4", "C5") if not out[k].get("pass")]
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print(json.dumps({k: out[k].get("pass") for k in ("C1", "C2", "C3", "C4", "C5")}), "all_pass:", out["all_pass"])


if __name__ == "__main__":
    main(sys.argv[1:])
