import numpy as np
from pathlib import Path

# 1. 실제 데이터 경로 (주신 경로 정보를 바탕으로 수정함)
PDB_DIR = Path("/home/ktkim/AllerScope_raw/data/processed/fungal_allergen_pdb/pdb")
MATRIX_PATH = Path("/home/ktkim/AllerScope_raw/data/processed/manifold/protein_tm_distance_matrix.npy")

def main():
    # 2. PDB 파일 리스트를 정렬하여 ID 목록 생성
    # npy를 만들 때와 동일한 sorted()를 사용하여 인덱스 순서를 맞춥니다.
    if not PDB_DIR.exists():
        print(f"❌ Error: PDB 디렉토리를 찾을 수 없습니다: {PDB_DIR}")
        return

    # 파일명에서 .pdb만 떼어내고 리스트화
    pdb_files = sorted(PDB_DIR.glob("*.pdb"))
    protein_ids = [f.stem for f in pdb_files]
    
    # 3. .npy 행렬 로드
    if not MATRIX_PATH.exists():
        print(f"❌ Error: npy 파일을 찾을 수 없습니다: {MATRIX_PATH}")
        return
        
    matrix = np.load(MATRIX_PATH)
    print(f"✅ 데이터 로드 완료 (Matrix Shape: {matrix.shape})")

    # 4. 찾고자 하는 ID 설정
    id_row = "Q0CJH1"
    id_col = "P0C1B"

    try:
        # 리스트에서 ID의 위치(Index) 찾기
        row_idx = protein_ids.index(id_row)
        col_idx = protein_ids.index(id_col)
        
        # 행렬에서 해당 좌표의 값 추출
        val = matrix[row_idx, col_idx]
        
        print("\n" + "="*40)
        print(f"📍 검색 결과")
        print(f"행 ID: {id_row} (인덱스: {row_idx})")
        print(f"열 ID: {id_col} (인덱스: {col_idx})")
        print(f"값 (Distance): {val}")
        print("="*40)
        
    except ValueError:
        print(f"❌ Error: ID '{id_row}' 또는 '{id_col}'를 목록에서 찾을 수 없습니다.")
        print(f"샘플 ID (앞 5개): {protein_ids[:5]}")

if __name__ == "__main__":
    main()