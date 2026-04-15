"""Step 1b, ensemble orchestrator for the 14-member FORESEE-HUN EURO-CORDEX.

Runs the single-member pipeline (s01 -> s02 -> s03 -> s04) once per RCM
member against the flat ensemble archive at ``d:/FORESEE_1950-2100/``.

Archive layout
--------------
The ensemble archive is a **flat** directory with two file families:

- **Observed** (shared across all members):
  ``FORESEE_HUN_v1.1_observed_1971-2022_{tmax,tmin,pr,...}.nc``
- **Per-member RCP** (2022-2100 projections):
  ``<MEMBER>_FORESEE_HUN_v1.0_Corrected_{rcp45,rcp85}_2022-2100_{tasmax,tasmin,pr}.nc``

The pipeline's I/O layer (``common.foresee_io.list_foresee_files``) honours
the ``ENSEMBLE_MEMBER`` env var by filtering RCP files to only those whose
basename begins with the member prefix, so a single ``FORESEE_DIR`` can host
all members.

Each member gets its own output hierarchy under
``analysis/interim/ensemble/<member>/`` and
``analysis/curated/ensemble/<member>/``, driven by the ``ENSEMBLE_SUBDIR``
env var honoured by s01/s02/s03/s04.

Concurrency
-----------
Members are processed in parallel via subprocesses (one per member). The
weight matrix (``analysis/interim/district_weights.npz``) is shared across
members because the 0.1 deg grid is identical; it is built once on the
first member and reused.

Usage
-----
::

    python analysis/src/s01b_ensemble_orchestrator.py
    python analysis/src/s01b_ensemble_orchestrator.py --workers 6
    python analysis/src/s01b_ensemble_orchestrator.py --members CNRM_ALADIN53,CNRM_CCLM --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
ENSEMBLE_ROOT_DEFAULT = Path(r"D:/FORESEE_1950-2100")
MANIFEST_PATH = ANALYSIS / "curated" / "ensemble" / "ensemble_manifest.json"
INTERIM_ENSEMBLE = ANALYSIS / "interim" / "ensemble"
CURATED_ENSEMBLE = ANALYSIS / "curated" / "ensemble"

# Minimum size for a non-truncated daily NetCDF (a full 79-year RCP file is
# ~228 MB).
MIN_NC_BYTES = 150 * 1024 * 1024

REQUIRED_VARS = ("tasmax", "tasmin", "pr")
REQUIRED_SCENARIOS = ("rcp45", "rcp85")

# Filename pattern for RCP files in the flat archive.
MEMBER_RE = re.compile(
    r"^(?P<member>[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)+?)"
    r"_FORESEE_HUN_v1\.0_Corrected_(?P<scen>rcp\d+)_2022-2100_(?P<var>tasmax|tasmin|pr)\.nc$"
)


# ---------------------------------------------------------------------------
# Member discovery
# ---------------------------------------------------------------------------

def discover_members(root: Path) -> list[str]:
    """Return the sorted list of member prefixes present in the flat archive."""
    if not root.exists():
        raise FileNotFoundError(f"ensemble root not found: {root}")
    members: set[str] = set()
    for p in root.glob("*.nc"):
        m = MEMBER_RE.match(p.name)
        if m:
            members.add(m.group("member"))
    return sorted(members)


def audit_member(root: Path, member: str) -> dict:
    """Verify that every (var, scenario) combination is present and complete."""
    missing: list[str] = []
    undersized: list[str] = []
    files: dict[str, str] = {}
    for scen in REQUIRED_SCENARIOS:
        for var in REQUIRED_VARS:
            name = f"{member}_FORESEE_HUN_v1.0_Corrected_{scen}_2022-2100_{var}.nc"
            p = root / name
            if not p.exists():
                missing.append(f"{scen}/{var}")
                continue
            files[f"{scen}_{var}"] = str(p)
            if p.stat().st_size < MIN_NC_BYTES:
                undersized.append(f"{name} ({p.stat().st_size/1e6:.1f} MB)")
    complete = not missing and not undersized
    return {"member": member, "complete": complete,
            "missing": missing, "undersized": undersized, "files": files}


# ---------------------------------------------------------------------------
# Per-member worker
# ---------------------------------------------------------------------------

def _run_stage(script: str, env: dict, log_path: Path, cwd: Path) -> int:
    with open(log_path, "w", encoding="utf-8") as logf:
        return subprocess.call(
            [sys.executable, script],
            env=env, stdout=logf, stderr=subprocess.STDOUT, cwd=str(cwd),
        )


def _member_worker(member: str, ensemble_root: str, analysis_dir: str,
                   stages: tuple[str, ...]) -> dict:
    """Run the pipeline stages for one RCM member in a fresh subprocess."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["FORESEE_DIR"] = ensemble_root
    env["ENSEMBLE_MEMBER"] = member
    env["ENSEMBLE_SUBDIR"] = f"ensemble/{member}"
    env["PYTHONPATH"] = str(Path(analysis_dir) / "src") + os.pathsep + env.get("PYTHONPATH", "")

    log_dir = Path(analysis_dir) / "interim" / "ensemble" / member / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    for tag in stages:
        script = str(Path(analysis_dir) / "src" / {
            "s01": "s01_extract_daily_districts.py",
            "s02": "s02_compute_indices.py",
            "s03": "s03_normals_and_anomalies.py",
            "s04": "s04_variety_match.py",
        }[tag])
        rc = _run_stage(script, env, log_dir / f"{tag}.log", Path(analysis_dir))
        if rc != 0:
            return {"member": member, "status": "failed",
                    "failed_stage": tag, "log_dir": str(log_dir),
                    "elapsed_s": round(time.time() - t0, 1)}

    return {"member": member, "status": "ok",
            "elapsed_s": round(time.time() - t0, 1),
            "log_dir": str(log_dir),
            "interim": str(Path(analysis_dir) / "interim" / "ensemble" / member),
            "curated": str(Path(analysis_dir) / "curated" / "ensemble" / member)}


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def write_manifest(processed: list[dict], missing: list[dict],
                   ensemble_root: Path, stages: tuple[str, ...]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ensemble_root": str(ensemble_root),
        "stages": list(stages),
        "n_members_processed": len(processed),
        "n_members_missing": len(missing),
        "members_processed": processed,
        "members_missing": missing,
    }
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[s01b] manifest -> {MANIFEST_PATH}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ensemble-root", type=Path, default=ENSEMBLE_ROOT_DEFAULT,
                    help="flat directory with observed + per-member RCP NetCDFs")
    ap.add_argument("--members", type=str, default=None,
                    help="comma-separated subset of member prefixes (default: all discovered)")
    ap.add_argument("--workers", type=int, default=4,
                    help="number of members processed in parallel")
    ap.add_argument("--stages", type=str, default="s01,s02,s03,s04",
                    help="comma-separated pipeline stages to run")
    ap.add_argument("--dry-run", action="store_true",
                    help="audit members and print plan, do not execute")
    args = ap.parse_args()

    root = args.ensemble_root
    stages = tuple(s.strip() for s in args.stages.split(",") if s.strip())

    print(f"[s01b] ensemble root: {root}")
    all_members = discover_members(root)
    print(f"[s01b] discovered {len(all_members)} members: {all_members}")

    wanted = [m.strip() for m in (args.members.split(",") if args.members else all_members)
              if m.strip()]
    audits = [audit_member(root, m) for m in wanted]
    complete = [a for a in audits if a["complete"]]
    incomplete = [a for a in audits if not a["complete"]]

    print(f"[s01b] {len(complete)} complete, {len(incomplete)} incomplete")
    for a in incomplete:
        print(f"[s01b] SKIP {a['member']}: missing={a['missing']} undersized={a['undersized']}")

    if args.dry_run:
        for a in complete:
            print(f"[s01b] would run {'->'.join(stages)} for {a['member']}")
        return

    INTERIM_ENSEMBLE.mkdir(parents=True, exist_ok=True)
    CURATED_ENSEMBLE.mkdir(parents=True, exist_ok=True)

    # Run the first member alone to populate the shared weight matrix,
    # then parallelise the rest.
    processed: list[dict] = []
    failed: list[dict] = []

    if not complete:
        print("[s01b] no complete members to process")
        write_manifest(processed, incomplete, root, stages)
        return

    first = complete[0]
    rest = complete[1:]

    t0 = time.time()
    weights_npz = ANALYSIS / "interim" / "district_weights.npz"
    if not weights_npz.exists():
        print(f"[s01b] priming weight matrix with {first['member']} (serial)...")
        res = _member_worker(first["member"], str(root), str(ANALYSIS.parent / "analysis"),
                             stages=stages)
        (processed if res["status"] == "ok" else failed).append(res)
        complete_to_run = rest
    else:
        print(f"[s01b] weight matrix exists, running all {len(complete)} members in parallel")
        complete_to_run = complete

    if complete_to_run:
        with ProcessPoolExecutor(max_workers=args.workers) as ex:
            futs = {
                ex.submit(_member_worker, a["member"], str(root),
                          str(ANALYSIS.parent / "analysis"), stages): a["member"]
                for a in complete_to_run
            }
            for fut in as_completed(futs):
                member = futs[fut]
                try:
                    res = fut.result()
                except Exception as e:
                    failed.append({"member": member, "status": "launch_error",
                                   "error": repr(e)})
                    continue
                print(f"[s01b] done {member}: {res['status']} in {res['elapsed_s']}s")
                (processed if res["status"] == "ok" else failed).append(res)

    print(f"[s01b] total wall time: {time.time()-t0:.1f}s")
    missing = incomplete + failed
    write_manifest(processed, missing, root, stages)


if __name__ == "__main__":
    main()
