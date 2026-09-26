#### Hệ thống Images to Category
# Mô tả:
    - Input: Người dùng chụp 1 hoặc vài tấm ảnh vào hệ thống + text mô tả hình ảnh từ người dùng (nếu có)
    - Output: Hệ thống sử dụng CLIP để vector hóa ảnh + text -> truy xuất vào FAISS rồi trả về danh mục của sản phẩm đó + viết lại 1 đoạn text mô tả sản phẩm (VD: Thiết bị điện tử > Điện thoại > Samsung > Samsung s25 ultra đen)
    Dataset: Cell_Phones_and_Accessories (35k dòng chính) + Appliances (5k dòng - với nhiệm vụ làm nhiễu cho model)
    - Mục đích là Với 2 dataset khác nhau thì khi tạo FAISS sẽ chia thành 2 cụm riêng biệt
# Điểm vượt trội của hệ thống:
    - Khi người dùng chụp ảnh sản phẩm mà sản phẩm không thuộc Ngành hàng điện thoại và phụ kiện thì sẽ in ra text: "Có vẻ như sản phẩm bạn chọn không được hỗ trợ, hãy chọn ảnh sản phẩm khác" bằng cách tính khoảng cách trong faiss nếu quá xa Cell_Phones hoặc quá gần Appliances hoặc quá xa thì sẽ in ra như vậy. Sử dụng thuật toán ngưỡng thích ứng bằng xác suất chứ không fix cứng
    - Hệ thống tự học: ví dụ Khi hệ thống phát hiện đó là cái điện thoại nhưng ko biết chính xác model nào thì sẽ yêu cầu người dùng nhập cụ thể tên sản phẩm rồi hệ thống sẽ vector hóa ảnh + text đó đưa vào trong faiss theo thời gian thực

### Tiến độ đồ án
    - Bước 1: Data preparation + Clean: Đã xong
        + Tải dataset: Lọc ra 35k + 5k và trộn lại
        + Lọc ra các dòng đạt điều kiện (cột images(main + pt1) không được null)
        + Lọc tiếp bằng cách tải ảnh từ url xuống nếu lỗi sẽ loại bỏ dòng đó
        + Áp dụng padding viền trắng + Resize lại ảnh về 224x224 (chuẩn CLIP)
    - Bước 2: Tạo FAISS: Đang thực hiện 
        + Tạo dataset trên kaggle (folder resized_images + final_metadata.jsonl): Đã xong

### Quản lý đồ án
    - Sau khi thực hiện xong bước 1 thì phải đem lên Kaggle chạy vì máy local yếu. Quy trình như sau:
        + Push code lên github
        + Rồi từ Kaggle kéo code về và chạy bước 2

   ====GỢI Ý TỪ GEMINI====
    Quy trình chuẩn hóa đầy đủ trên Kaggle sẽ như sau:

Đồng bộ mã nguồn (Input Code): Trên Kaggle Notebook, thay vì copy/paste code thủ công, bạn dùng lệnh !git clone [link_github_của_bạn] để kéo toàn bộ các file .py hoặc script cấu hình về môi trường Kaggle. 

Kết nối Dữ liệu (Input Data): Add cái Dataset 550MB (gồm folder ảnh và file CSV/JSONL) mà bạn đã upload vào thẳng Notebook.

Chạy thực nghiệm GPU (Execution): Bật bộ tăng tốc GPU (P100 hoặc T4 x2) của Kaggle lên, chạy mô hình CLIP để sinh vector và nạp vào không gian FAISS.

Khóa đuôi dữ liệu (Output - Mắt xích bạn đang thiếu): Khi luồng code chạy xong, nó sẽ sinh ra một tập tin vật lý cực kỳ quan trọng (ví dụ: amazon_c2c.index - chứa ma trận vector của FAISS) và có thể là một file mapping_id.pkl. Môi trường Kaggle là tạm thời, nếu bạn tắt trình duyệt, các file sinh ra này sẽ bị xóa sạch. Do đó, dòng code cuối cùng của bạn phải là lệnh tải hai file này về lại máy Local, hoặc lưu trực tiếp chúng thành một Kaggle Output Dataset mới.