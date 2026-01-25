#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

import numpy as np

PDB_DIR = Path("/home/ktkim/AllerScope_raw/data/processed/epitope/pdb")
TMALIGN_BIN = Path("/home/ktkim/miniconda3/envs/aller/bin/TMalign")
OUT_DIR = Path("/home/ktkim/AllerScope_raw/data/processed/manifold")
MAX_WORKERS = 8

TM_RE = re.compile(r"TM-score\s*=\s*([0-9.]+)")

def run_tmalign(task):
    i, j, p1, p2 = task
    res = subprocess.run(
        [str(TMALIGN_BIN), p1, p2],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if res.returncode != 0:
        raise RuntimeError(
            f"TMalign failed for {Path(p1).name} vs {Path(p2).name}\n"
            f"STDERR:\n{res.stderr}"
        )

    scores = TM_RE.findall(res.stdout)
    if len(scores) < 2:
        raise RuntimeError(
            f"Only {len(scores)} TM-scores for {Path(p1).name} vs {Path(p2).name}"
        )

    score = 0.5 * (float(scores[0]) + float(scores[1]))
    return i, j, score


def task_iter(pdb_files):
    n = len(pdb_files)
    for i in range(n):
        p1 = str(pdb_files[i])
        for j in range(i + 1, n):
            yield (i, j, p1, str(pdb_files[j]))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pdb_files = sorted(PDB_DIR.glob("*.pdb"))
    n = len(pdb_files)
    print(f"Found {n} PDB files")
    if n == 0:
        raise SystemExit(f"No PDB files found in {PDB_DIR}")

    total = n * (n - 1) // 2
    print(f"Total pairwise comparisons: {total}")
    if total == 0:
        return

    tm_mat = np.zeros((n, n), dtype=float)
    np.fill_diagonal(tm_mat, 1.0)

    done = 0
    report_every = max(1, total // 100)

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as ex:
        for i, j, score in ex.map(run_tmalign, task_iter(pdb_files), chunksize=50):
            tm_mat[i, j] = score
            tm_mat[j, i] = score

            done += 1
            if done % report_every == 0 or done == total:
                print(f"Progress: {done}/{total} ({done/total*100:.1f}%)", flush=True)

    dist_mat = 1.0 - tm_mat

    np.save(OUT_DIR / "epitope_tm_score_matrix.npy", tm_mat)
    np.save(OUT_DIR / "epitope_tm_distance_matrix.npy", dist_mat)

    print(f"TM-score matrix : {OUT_DIR / 'epitope_tm_score_matrix.npy'}")
    print(f"Distance matrix : {OUT_DIR / 'epitope_tm_distance_matrix.npy'}")


if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    main()
