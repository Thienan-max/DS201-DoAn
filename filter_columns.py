import json
import os

INPUT_PATH = "data/processed_data/cleaned_data.jsonl"
OUTPUT_PATH = "data/processed_data/final_metadata.jsonl"

def process_file():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: Khong tim thay file {INPUT_PATH}")
        return
        
    print(f"Dang doc va loc cot tu {INPUT_PATH}...")
    
    count = 0
    with open(INPUT_PATH, 'r', encoding='utf-8') as infile, open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                row = json.loads(line)
                
                # Lấy color từ trong object "details" (vì Amazon thường lưu color ở đây)
                details = row.get("details") or {}
                color = details.get("Color") or details.get("color") or ""
                
                # Tạo object mới chỉ chứa đúng các cột bạn yêu cầu
                new_row = {
                    "parent_asin": row.get("parent_asin", ""),
                    "title": row.get("title", ""),
                    "main_category": row.get("main_category", ""),
                    "features": row.get("features", []),
                    "description": row.get("description", []),
                    "color": color
                }
                
                # Ghi dòng dữ liệu mới ra file
                outfile.write(json.dumps(new_row, ensure_ascii=False) + "\n")
                count += 1
            except Exception as e:
                continue
                
    print(f"XONG! Da giu lai {count} dong du lieu.")
    print(f"File du lieu sieu nhe da duoc luu tai: {OUTPUT_PATH}")

if __name__ == "__main__":
    process_file()
