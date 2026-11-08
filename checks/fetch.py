#!/usr/bin/env python3
"""C1: fetch the nine files of hanxinzhang/prime-bound at the pinned commit into an isolated directory, record
sha256 and size for each, and statically list the modules imported by the quick-check path. No downloaded code is
executed here. usage: fetch.py OUT_DIR"""
import hashlib, json, os, re, sys, urllib.request

COMMIT = "2319570b0056676537190512f20af80d3a7b72a7"
FILES = {"README.md": 7308, "data/certificate.json": 295566, "data/event_cells.json": 1421597, "data/source_polynomial.json": 537094,
         "data/stored_marginal.json": 614291, "requirements-full.txt": 20, "src/exact_core.py": 14802, "src/full_verify.py": 19234, "verify.py": 16985}
try:
    STDLIB = set(sys.stdlib_module_names)
except AttributeError:  # Python < 3.10 on the host
    import importlib.util
    def _is_stdlib(m):
        try:
            spec = importlib.util.find_spec(m)
        except (ImportError, ValueError):
            return False
        o = (spec.origin or "") if spec else ""
        return bool(spec) and ("site-packages" not in o) and ("dist-packages" not in o)
    class _S(set):
        def __contains__(self, m): return _is_stdlib(m)
    STDLIB = _S()


def main(out):
    os.makedirs(out, exist_ok=True)
    manifest = {"repo": "github.com/hanxinzhang/prime-bound", "commit": COMMIT, "files": {}, "imports": {}}
    for path, size in FILES.items():
        url = f"https://raw.githubusercontent.com/hanxinzhang/prime-bound/{COMMIT}/{path}"
        data = urllib.request.urlopen(url, timeout=120).read()
        dest = os.path.join(out, path); os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(data)
        manifest["files"][path] = {"bytes": len(data), "expected_bytes": size, "size_ok": len(data) == size, "sha256": hashlib.sha256(data).hexdigest()}
    for path in ("verify.py", "src/exact_core.py", "src/full_verify.py"):
        text = open(os.path.join(out, path), encoding="utf-8", errors="replace").read()
        mods = sorted({m.split(".")[0] for m in re.findall(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", text, re.M) for m in m if m})
        manifest["imports"][path] = {"modules": mods, "non_stdlib": [m for m in mods if m not in STDLIB and m not in ("src", "exact_core", "full_verify")]}
    manifest["requirements_full"] = open(os.path.join(out, "requirements-full.txt")).read().strip().splitlines()
    manifest["all_sizes_ok"] = all(f["size_ok"] for f in manifest["files"].values())
    json.dump(manifest, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest.json"), "w"), indent=1)
    print(json.dumps({k: manifest[k] for k in ("all_sizes_ok", "imports", "requirements_full")}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
