import json
import random
import os

def is_valid(row):
    if not row.get("title") or not str(row.get("title")).strip():
        return False
    if not row.get("main_category") or not str(row.get("main_category")).strip():
        return False
    if not row.get("features") or len(row.get("features")) == 0:
        return False
    if not row.get("description") or len(row.get("description")) == 0:
        return False
    images = row.get("images")
    if not images or len(images) == 0:
        return False
    has_hi_res = any(img.get("hi_res") and str(img.get("hi_res")).strip() for img in images)
    if not has_hi_res:
        return False
    return True

def reservoir_sample(filepath, k, seed=42):
    random.seed(seed)
    reservoir = []
    count = 0
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                row = json.loads(line)
            except:
                continue
                
            if is_valid(row):
                if count < k:
                    reservoir.append(line)
                else:
                    j = random.randint(0, count)
                    if j < k:
                        reservoir[j] = line
                count += 1
                
    print(f"Total valid rows found: {count}. Sampled: {len(reservoir)}")
    if count < k:
        print(f"Warning: Only found {count} valid rows, requested {k}.")
    return reservoir

def main():
    phones_path = "data/raw_data/meta_Cell_Phones_and_Accessories.jsonl/meta_Cell_Phones_and_Accessories.jsonl"
    appliances_path = "data/raw_data/meta_Appliances.jsonl/meta_Appliances.jsonl"
    out_path = "data/processed_data/filtered_data.jsonl"
    
    os.makedirs("data/processed_data", exist_ok=True)
    
    sampled_phones = reservoir_sample(phones_path, 35000)
    sampled_appliances = reservoir_sample(appliances_path, 5000)
    
    all_sampled = sampled_phones + sampled_appliances
    random.seed(42)
    random.shuffle(all_sampled)
    
    print(f"Writing {len(all_sampled)} rows to {out_path}...")
    with open(out_path, 'w', encoding='utf-8') as f:
        for line in all_sampled:
            f.write(line)
            
    print("Done! Data saved to", out_path)

if __name__ == "__main__":
    main()
