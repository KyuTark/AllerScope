#!/usr/bin/env python3

import os
import glob
import pandas as pd

DATADIR = os.path.expanduser("/AllerScope/data")
PDB_DIR = f"{DATADIR}/fungal_allergen/pdb"
BEP_DIR = f"{DATADIR}/epitope/bepipred"
DIS_DIR = f"{DATADIR}/epitope/discotope"
OUT_DIR = f"{DATADIR}/epitope/epitope_pdb"

THRESH_BEPI = 0.1512
# Discotope epitope == True
CHAIN = "A"
pdb_paths = sorted(glob.glob(os.path.join(PDB_DIR, "*.pdb")))

for pdb_path in pdb_paths:
    name = os.path.splitext(os.path.basename(pdb_path))[0]

    bepi_csv = os.path.join(BEP_DIR, name, "raw_output.csv")
    if not os.path.exists(bepi_csv):
        continue

    dis_pat = os.path.join(DIS_DIR, name, "**", f"{name}_{CHAIN}_discotope3.csv")
    dis_hits = sorted(glob.glob(dis_pat, recursive=True))
    if not dis_hits:
        continue
    dis_csv = dis_hits[0]

    df_b = pd.read_csv(bepi_csv)
    b = df_b["BepiPred-3.0 score"].astype(float).to_numpy()

    df_d = pd.read_csv(dis_csv)
    res_id = df_d["res_id"].astype(int).to_numpy()
    epi = (
        df_d["epitope"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "t", "yes", "y"])
        .to_numpy()
        )

    keep_res = set()
    keep_res.update([i for i, score in enumerate(b, start=1) if score >= THRESH_BEPI])
    keep_res.update(res_id[epi].tolist())

    out_pdb = os.path.join(OUT_DIR, f"epi_{name}.pdb")

    kept_seen = set()
    with open(pdb_path, "r") as fr, open(out_pdb, "w") as fw:
        for line in fr:
            rec = line[:6].strip()
            if rec in {"ATOM", "HETATM"}:
                ch = line[21:22]
                if ch != CHAIN:
                    continue
                resseq_str = line[22:26].strip()
                if not resseq_str:
                    continue
                resseq = int(resseq_str)
                if resseq in keep_res:
                    fw.write(line)
                    kept_seen.add(resseq)
            else:
                fw.write(line)

    print(f"[DONE] {name} -> {out_pdb}")