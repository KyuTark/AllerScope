# Run DiscoTope 3.0

cd ${HOME}/AllerScope/src/workdir/DiscoTope-3.0

python discotope3/main.py \
  --pdb_or_zip_file ${HOME}/AllerScope/data/fungal_allergen/pdb/ref001.pdb \
  --struc_type alphafold \
  --out_dir ${HOME}/AllerScope/data/epitope/discotope
