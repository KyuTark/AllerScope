#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/AllerScope/src/workdir"
CACHE="/AllerScope/colabfold_cache"
IMAGE="ghcr.io/sokrypton/colabfold:1.5.5-cuda12.2.2"

DATA_DIR="/AllerScope/data/FungalAllergen/fasta"
OUT_ROOT="${WORKDIR}/structures_raw"
MSA_ARGS=""  # e.g., "--msa-mode single_sequence"

IN_DIR="${WORKDIR}/_inputs"
mkdir -p "${IN_DIR}" "${OUT_ROOT}" "${CACHE}"
cd "${WORKDIR}"

shopt -s nullglob
FILES=("${DATA_DIR}"/*.fasta)

for f in "${FILES[@]}"; do
  bn="$(basename "$f")"
  stem="${bn%.*}"
  in_local="${IN_DIR}/${stem}.fasta"
  out_dir="${OUT_ROOT}/${stem}"
  mkdir -p "${out_dir}"

  awk -v pfx="${stem}" '
    BEGIN{n=0}
    /^>/ { n++; printf(">%s_%04d\n", pfx, n); next }
    { print }
  ' "$f" > "$in_local"

  echo "[RUN] ${bn} -> ${out_dir}"

  docker run --rm --gpus all \
    --user "$(id -u):$(id -g)" \
    -v "${CACHE}:/cache:rw" \
    -v "${WORKDIR}:/work:rw" \
    "${IMAGE}" \
    colabfold_batch ${MSA_ARGS} "/work/_inputs/${stem}.fasta" "/work/structures_raw/${stem}"
done

echo "[DONE] OUT_ROOT=${OUT_ROOT}"
