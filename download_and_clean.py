import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

DATA_PATH = "data/processed_data/filtered_data.jsonl"
IMAGE_DIR = "data/images"
CLEAN_DATA_PATH = "data/processed_data/cleaned_data.jsonl"
MAX_WORKERS = 32

def download_image(url, save_path):
    if os.path.exists(save_path):
        if os.path.getsize(save_path) > 1024:
            return True
            
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            if os.path.getsize(save_path) > 1024:
                return True
            else:
                os.remove(save_path)
                return False
    except Exception:
        return False
    return False

def process_row(line):
    try:
        row = json.loads(line)
        asin = row.get("parent_asin")
        if not asin:
            return None
            
        images = row.get("images", [])
        main_url = None
        pt01_url = None
        
        for img in images:
            if img.get("variant") == "MAIN":
                main_url = img.get("hi_res") or img.get("large")
            elif img.get("variant") == "PT01":
                pt01_url = img.get("hi_res") or img.get("large")
                
        if not main_url:
            return None
            
        main_path = os.path.join(IMAGE_DIR, f"{asin}_1.jpg")
        main_success = download_image(main_url, main_path)
        
        if not main_success:
            return None
            
        if pt01_url:
            pt01_path = os.path.join(IMAGE_DIR, f"{asin}_2.jpg")
            pt01_success = download_image(pt01_url, pt01_path)
            if not pt01_success:
                if os.path.exists(main_path):
                    os.remove(main_path)
                return None
                
        return line
    except Exception:
        return None

def main():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    print(f"Reading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: File {DATA_PATH} not found.")
        return
        
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print(f"Total rows to process: {len(lines)}")
    valid_lines = []
    
    print("Starting download process (this may take a long time)...")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_row, line) for line in lines]
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            res = future.result()
            if res is not None:
                valid_lines.append(res)
                
            if completed % 1000 == 0:
                print(f"Processed {completed}/{len(lines)} rows. Valid rows so far: {len(valid_lines)}")

    print("==================================================")
    print(f"Finished downloading and cleaning! Final valid rows: {len(valid_lines)}")
    
    print(f"Saving cleaned data to {CLEAN_DATA_PATH}...")
    with open(CLEAN_DATA_PATH, 'w', encoding='utf-8') as f:
        for line in valid_lines:
            f.write(line)
            
    print("DONE! Images are in data/images")

if __name__ == "__main__":
    main()
