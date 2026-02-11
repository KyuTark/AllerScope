import numpy as np
from pathlib import Path

PDB_DIR = Path("/AllerScope/data/processed/fungal_allergen_pdb/pdb")
MATRIX_PATH = Path("/AllerScope/data/processed/manifold/protein_tm_distance_matrix.npy")

def main():
    pdb_files = sorted(PDB_DIR.glob("*.pdb"))
    protein_ids = [f.stem for f in pdb_files]
    
    matrix = np.load(MATRIX_PATH)

    id_row = "Q0CJH1"
    id_col = "P0C1B"

    try:
        row_idx = protein_ids.index(id_row)
        col_idx = protein_ids.index(id_col)
        
        val = matrix[row_idx, col_idx]
        
        print("\n" + "="*40)
        print(f"RESULT")
        print(f"row ID: {id_row} (idx: {row_idx})")
        print(f"col ID: {id_col} (idx: {col_idx})")
        print(f"val (Distance): {val}")
        print("="*40)
        
    except ValueError:
        print(f"Error: ID '{id_row}' or '{id_col}' are not in the list")
        print(f"sample ID (5): {protein_ids[:5]}")

if __name__ == "__main__":
    main()