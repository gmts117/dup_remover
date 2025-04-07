import os
import hashlib

def calculate_file_hash(file_path):
    """파일의 SHA-256 해시를 계산"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def find_and_select_duplicates(root_path):
    """중복 파일 탐색 후 사용자에게 선택하여 삭제하도록 요청"""
    file_hashes = {}
    duplicates = {}

    # 1단계: 중복 파일 찾기
    for root, dirs, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            
            if file_hash in file_hashes:
                if file_hash not in duplicates:
                    duplicates[file_hash] = [file_hashes[file_hash]]
                duplicates[file_hash].append(file_path)
            else:
                file_hashes[file_hash] = file_path

    # 2단계: 중복 파일이 없는 경우 처리
    if not duplicates:
        print("중복 파일이 없습니다.")
        return

    print(f"총 {len(duplicates)} 개의 중복 파일 그룹을 발견했습니다.")
    
    # 3단계: 삭제 방식 선택
    print("\n삭제 방식을 선택하세요:")
    print("1. 수동 선택 (개별 파일 선택)")
    print("2. 자동 삭제 (각 그룹에서 하나만 남기고 모두 삭제)")
    choice = input("선택 (1 또는 2): ").strip()
    
    if choice == "2":
        # 자동 삭제 모드
        auto_delete_duplicates(duplicates)
    else:
        # 수동 선택 모드 (기존 기능)
        manual_delete_duplicates(duplicates)

def auto_delete_duplicates(duplicates):
    """각 중복 그룹에서 하나만 남기고 나머지 자동 삭제"""
    total_deleted = 0
    total_kept = 0
    
    print("\n자동 삭제 모드를 시작합니다...")
    
    for file_hash, paths in duplicates.items():
        # 첫 번째 파일은 보존
        keep_file = paths[0]
        total_kept += 1
        
        # 나머지 파일은 삭제
        for path in paths[1:]:
            os.remove(path)
            print(f"삭제됨: {path}")
            total_deleted += 1
        
        print(f"보존됨: {keep_file}")
    
    print(f"\n자동 삭제 완료: {total_deleted}개 파일 삭제, {total_kept}개 파일 보존")

def manual_delete_duplicates(duplicates):
    """사용자가 직접 삭제할 파일을 선택"""
    file_to_index = {}
    index = 1
    print("\n중복 파일 목록:")
    for file_hash, paths in duplicates.items():
        print(f"\n해시: {file_hash}")
        for path in paths:
            file_to_index[index] = path
            print(f"  {index}. {path}")
            index += 1

    # 사용자에게 삭제할 파일 선택 요청
    selected_indices = input("\n삭제할 파일 번호를 쉼표로 구분하여 입력하세요 (예: 1,3,5): ").strip()
    selected_indices = selected_indices.split(',')
    
    files_to_delete = []
    for index_str in selected_indices:
        try:
            index = int(index_str)
            if index in file_to_index:
                files_to_delete.append(file_to_index[index])
            else:
                print(f"잘못된 번호: {index}")
        except ValueError:
            print(f"잘못된 입력: {index_str}")

    if files_to_delete:
        # 파일 삭제
        for file_path in files_to_delete:
            os.remove(file_path)
            print(f"삭제됨: {file_path}")
        print(f"선택된 {len(files_to_delete)}개 중복 파일 삭제가 완료되었습니다.")
    else:
        print("삭제할 파일이 없습니다.")

def main():
    """사용자로부터 경로를 입력받아 중복 파일 제거"""
    path = input("중복 파일을 확인할 디렉토리 경로를 입력하세요: ").strip()
    if os.path.isdir(path):
        find_and_select_duplicates(path)
    else:
        print("유효한 디렉토리 경로가 아닙니다.")

if __name__ == "__main__":
    main()
