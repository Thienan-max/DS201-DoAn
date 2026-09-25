import os
import json
import re
import html
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

RESIZED_DIR = "data/resized_images"
METADATA_PATH = "data/processed_data/final_metadata.jsonl"
CLEAN_METADATA_PATH = "data/processed_data/final_metadata_clean.jsonl"
MAX_WORKERS = 16

def clean_title(text):
    if not isinstance(text, str):
        return ""
    # Decode HTML entities like &amp;, &quot;
    text = html.unescape(text)
    # Remove HTML tags like <br>, <b>
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove emojis and non-ascii (keeping only basic ascii)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def check_image(filename):
    filepath = os.path.join(RESIZED_DIR, filename)
    try:
        with Image.open(filepath) as img:
            img.verify()
        return filename, True
    except Exception:
        return filename, False

def main():
    print("Step 1: Quét ảnh thây ma (Corrupted Images)...")
    images = [f for f in os.listdir(RESIZED_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
    corrupted_images = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_image, f) for f in images]
        completed = 0
        for future in as_completed(futures):
            filename, is_valid = future.result()
            if not is_valid:
                corrupted_images.append(filename)
            completed += 1
            if completed % 5000 == 0:
                print(f"  Đã quét {completed}/{len(images)} ảnh...")
                
    print(f"Phát hiện {len(corrupted_images)} ảnh lỗi.")
    corrupted_asins = set()
    for filename in corrupted_images:
        # Extract ASIN from filename (e.g. B0000_1.jpg -> B0000)
        asin = filename.split('_')[0]
        corrupted_asins.add(asin)
        filepath = os.path.join(RESIZED_DIR, filename)
        try:
            os.remove(filepath)
        except:
            pass

    print("Step 2 & 3: Khử mã HTML trong Title & Đồng bộ hóa mồ côi (Orphan Data Mismatch)...")
    # Remaining images
    remaining_images = [f for f in os.listdir(RESIZED_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
    image_asins = set(f.split('_')[0] for f in remaining_images)
    
    valid_rows = []
    metadata_asins = set()
    
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    row = json.loads(line)
                    asin = row.get("parent_asin")
                    if not asin:
                        continue
                    
                    # Remove if it was associated with a corrupted image
                    if asin in corrupted_asins:
                        continue
                        
                    # Remove if there are no corresponding images
                    if asin not in image_asins:
                        continue
                    
                    # Clean title
                    row["title"] = clean_title(row.get("title", ""))
                    
                    valid_rows.append(row)
                    metadata_asins.add(asin)
                except json.JSONDecodeError:
                    continue
                    
    # Now check for orphaned images (images without a row in metadata)
    orphaned_images = []
    for filename in remaining_images:
        asin = filename.split('_')[0]
        if asin not in metadata_asins:
            orphaned_images.append(filename)
            filepath = os.path.join(RESIZED_DIR, filename)
            try:
                os.remove(filepath)
            except:
                pass
                
    print(f"Đã xóa {len(orphaned_images)} ảnh mồ côi.")
    
    print(f"Đang lưu metadata đã được làm sạch...")
    with open(CLEAN_METADATA_PATH, 'w', encoding='utf-8') as f:
        for row in valid_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            
    # Thay thế file cũ
    os.replace(CLEAN_METADATA_PATH, METADATA_PATH)
    print(f"Hoàn thành! Giữ lại {len(valid_rows)} dòng dữ liệu.")
    print("Dữ liệu đã đạt chuẩn Cleaned (Production-ready).")

if __name__ == "__main__":
    main()
