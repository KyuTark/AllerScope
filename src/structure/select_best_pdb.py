#!/usr/bin/env python3

import os
import re
import glob
import shutil

WORKDIR = os.path.expanduser("~/AllerScope/src/workdir")
DATADIR = os.path.expanduser("~/AllerScope/data")
IN_DIR = f"{WORKDIR}/_inputs"
RAW_DIR = f"{WORKDIR}/structures_raw"
OUT_DIR = f"{DATADIR}/fungal_allergen/pdb"


def fasta_ids(fasta_path):
    ids = []
    with open(fasta_path) as f:
        for line in f:
            if line.startswith(">"):
                pid = re.split(r"\s+", line[1:].strip())[0]
                if pid:
                    ids.append(pid)
    return list(dict.fromkeys(ids))
    

def pick_best(pred_dir, pid):
    # Priority: 1) rank_001+relaxed 2) rank_001(any) 3) relaxed(any) 4) any pdb
    patterns = [
        f"{pid}*rank_001*relaxed*.pdb",
        f"{pid}*rank_001*.pdb",
        f"{pid}*relaxed*.pdb",
        f"{pid}*.pdb",
    ]
    for pat in patterns:
        hits = sorted(glob.glob(os.path.join(pred_dir, pat)))
        if hits:
            return hits[0]
    return None


def main():
    for fn in sorted(os.listdir(IN_DIR)):
        if not fn.endswith(".fasta"):
            continue

        stem = fn[:-6]  # remove ".fasta"
        fasta = os.path.join(IN_DIR, fn)
        pred_dir = os.path.join(RAW_DIR, stem)

        for pid in fasta_ids(fasta):
            best = pick_best(pred_dir, pid)
            if best is None:
                continue
            base = re.sub(r"_\d+$", "", pid)   # ref001_0001 -> ref001
            dst = os.path.join(OUT_DIR, f"{base}.pdb")
            shutil.copyfile(best, dst)
        print(f"DONE {stem}")


if __name__ == "__main__":
    main()
