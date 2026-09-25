import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_DIR = "data/images"
OUTPUT_DIR = "data/resized_images"
TARGET_SIZE = 224
MAX_WORKERS = 16  # Số luồng chạy song song

def process_image(filename):
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    # Bỏ qua nếu ảnh đã được xử lý (tiện cho việc chạy lại nếu rớt mạng/dừng giữa chừng)
    if os.path.exists(output_path):
        return True
        
    try:
        with Image.open(input_path) as img:
            # Chuyển đổi sang hệ màu RGB (để tránh lỗi đen viền với ảnh PNG có nền trong suốt)
            img = img.convert("RGB")
            
            width, height = img.size
            
            # 1. Tìm cạnh dài nhất để làm kích thước cho hình vuông nền
            max_dim = max(width, height)
            
            # 2. Tạo một hình vuông nền màu trắng hoàn toàn (255, 255, 255)
            square_img = Image.new("RGB", (max_dim, max_dim), (255, 255, 255))
            
            # 3. Tính toán vị trí x, y để dán ảnh gốc vào chính giữa hình vuông trắng
            paste_x = (max_dim - width) // 2
            paste_y = (max_dim - height) // 2
            
            # Dán ảnh gốc vào
            square_img.paste(img, (paste_x, paste_y))
            
            # 4. Resize hình vuông đó về kích thước chuẩn 224x224 của CLIP
            # Sử dụng thuật toán LANCZOS để giữ chi tiết tốt nhất khi thu nhỏ
            final_img = square_img.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
            
            # 5. Lưu ảnh đầu ra
            final_img.save(output_path, "JPEG", quality=90)
            return True
            
    except Exception as e:
        return False

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Thu muc {INPUT_DIR} khong ton tai!")
        return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Lấy danh sách toàn bộ ảnh trong thư mục
    filenames = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total_images = len(filenames)
    
    print(f"Tim thay {total_images} anh. Bat dau resize va them vien trang...")
    
    success_count = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_image, f) for f in filenames]
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            if future.result():
                success_count += 1
                
            if completed % 2000 == 0:
                print(f"Da xu ly {completed}/{total_images} anh...")
                
    print("==================================================")
    print(f"XONG! Da xu ly thanh cong {success_count}/{total_images} anh.")
    print(f"Anh da duoc luu tai: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
