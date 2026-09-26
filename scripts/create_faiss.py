import os
import json
import argparse
import torch
import faiss
import numpy as np
import pickle
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

class ProductDataset(Dataset):
    def __init__(self, metadata_path, image_dir):
        self.image_dir = image_dir
        self.data = []
        
        print("Đang đọc file metadata...")
        with open(metadata_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                asin = item.get("parent_asin")
                # Hỗ trợ lấy 2 ảnh: MAIN (_1) và PT01 (_2)
                img1_path = os.path.join(image_dir, f"{asin}_1.jpg")
                img2_path = os.path.join(image_dir, f"{asin}_2.jpg")
                
                # Chỉ lấy những mẫu có ảnh MAIN tồn tại
                if os.path.exists(img1_path):
                    self.data.append({
                        "id": asin,
                        "image_path_1": img1_path,
                        "image_path_2": img2_path if os.path.exists(img2_path) else img1_path,
                        "title": item.get("title", ""),
                        "category": item.get("main_category", ""),
                        "color": item.get("color", "")
                    })
        print(f"Tổng số sản phẩm hợp lệ: {len(self.data)}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        try:
            image1 = Image.open(item["image_path_1"]).convert("RGB")
        except Exception:
            # Tạo ảnh trắng nếu lỗi
            image1 = Image.new('RGB', (224, 224), (255, 255, 255))
            
        try:
            image2 = Image.open(item["image_path_2"]).convert("RGB")
        except Exception:
            image2 = image1 # Fallback về ảnh 1 nếu lỗi
            
        return {
            "id": item["id"],
            "image1": image1,
            "image2": image2,
            "title": item["title"],
            "category": item["category"],
            "color": item["color"]
        }

def collate_fn(batch, processor):
    images1 = [item["image1"] for item in batch]
    images2 = [item["image2"] for item in batch]
    
    # Kết hợp title và color để đưa vào CLIP
    texts = []
    colors = []
    for item in batch:
        text = item["title"]
        color = item.get("color", "")
        if color:
            text += f" - Color: {color}"
        texts.append(text)
        colors.append(color)
        
    ids = [item["id"] for item in batch]
    categories = [item["category"] for item in batch]
    
    inputs_text = processor(
        text=texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=77
    )
    
    # Xử lý 2 ảnh cùng lúc (nối danh sách 2 ảnh lại)
    inputs_images = processor(
        images=images1 + images2,
        return_tensors="pt"
    )
    
    return inputs_text, inputs_images, ids, categories, colors

def main(args):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Đang sử dụng device: {device}")

    # 1. Khởi tạo Model và Processor
    print(f"Đang tải model CLIP: {args.model_id}...")
    model = CLIPModel.from_pretrained(args.model_id).to(device)
    processor = CLIPProcessor.from_pretrained(args.model_id)
    model.eval()

    # 2. Khởi tạo Dataset và DataLoader
    dataset = ProductDataset(args.metadata_path, args.image_dir)
    dataloader = DataLoader(
        dataset, 
        batch_size=args.batch_size, 
        shuffle=False, 
        num_workers=4, 
        collate_fn=lambda b: collate_fn(b, processor)
    )

    # 3. Khởi tạo FAISS Index
    # CLIP base patch 32 có embedding size = 512
    d = 512
    
    # Dùng IndexFlatIP cho Cosine Similarity (Cần normalize vector trước khi thêm vào)
    # Nếu muốn dùng L2 distance thì dùng faiss.IndexFlatL2(d)
    index = faiss.IndexFlatIP(d) 
    
    # Res_faiss = faiss.StandardGpuResources()  # Có thể bật nếu dùng FAISS GPU
    # index = faiss.index_cpu_to_gpu(Res_faiss, 0, index)

    mapping_dict = {}
    current_index = 0

    print("Bắt đầu trích xuất đặc trưng và nạp vào FAISS...")
    with torch.no_grad():
        for batch_texts, batch_images, batch_ids, batch_categories, batch_colors in tqdm(dataloader):
            batch_texts = {k: v.to(device) for k, v in batch_texts.items()}
            batch_images = {k: v.to(device) for k, v in batch_images.items()}
            
            # Trích xuất đặc trưng ảnh (cho cả ảnh 1 và ảnh 2 cùng lúc) thủ công để đảm bảo luôn ra 512 chiều
            vision_outputs = model.vision_model(pixel_values=batch_images["pixel_values"])
            pooler_output = vision_outputs.pooler_output if hasattr(vision_outputs, 'pooler_output') else vision_outputs[1]
            all_image_features = model.visual_projection(pooler_output)
                    
            # Chia lại thành ảnh 1 và ảnh 2 rồi lấy trung bình
            bsz = len(batch_ids)
            image_features_1 = all_image_features[:bsz]
            image_features_2 = all_image_features[bsz:]
            image_features = (image_features_1 + image_features_2) / 2.0
            
            # Trích xuất đặc trưng văn bản thủ công
            text_outputs = model.text_model(input_ids=batch_texts["input_ids"], attention_mask=batch_texts["attention_mask"])
            text_pooler_output = text_outputs.pooler_output if hasattr(text_outputs, 'pooler_output') else text_outputs[1]
            text_features = model.text_projection(text_pooler_output)
            
            # (Tùy chọn) Kết hợp đặc trưng ảnh và văn bản: 
            # Có thể tính trung bình (average) giữa image và text vector
            combined_features = image_features + text_features
            
            # Chuẩn hóa (Normalize) vector để tính Cosine Similarity chính xác
            combined_features = combined_features / combined_features.norm(dim=-1, keepdim=True)
            
            # Chuyển về numpy để đưa vào FAISS
            embeddings = combined_features.cpu().numpy().astype('float32')
            
            # Thêm vào index
            index.add(embeddings)
            
            # Lưu mapping ID
            for i, (asin, category, color) in enumerate(zip(batch_ids, batch_categories, batch_colors)):
                mapping_dict[current_index + i] = {
                    "asin": asin,
                    "category": category,
                    "color": color
                }
            
            current_index += len(batch_ids)

    # 4. Lưu lại Index và Mapping
    print(f"Đã nạp xong {index.ntotal} vectors vào FAISS.")
    print(f"Đang lưu index vào {args.index_save_path}...")
    faiss.write_index(index, args.index_save_path)
    
    print(f"Đang lưu mapping id vào {args.mapping_save_path}...")
    with open(args.mapping_save_path, 'wb') as f:
        pickle.dump(mapping_dict, f)

    print("Hoàn tất! Hãy tải các file output về máy local.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo FAISS index từ ảnh và metadata")
    parser.add_argument("--image_dir", type=str, default="/kaggle/input/your-dataset-name/resized_images", help="Đường dẫn tới thư mục chứa ảnh")
    parser.add_argument("--metadata_path", type=str, default="/kaggle/input/your-dataset-name/final_metadata.jsonl", help="Đường dẫn tới file metadata")
    parser.add_argument("--index_save_path", type=str, default="amazon_c2c.index", help="Tên file lưu index")
    parser.add_argument("--mapping_save_path", type=str, default="mapping_id.pkl", help="Tên file lưu mapping ID")
    parser.add_argument("--batch_size", type=int, default=128, help="Kích thước batch")
    parser.add_argument("--model_id", type=str, default="openai/clip-vit-base-patch32", help="Tên model CLIP")
    
    args = parser.parse_args()
    main(args)
