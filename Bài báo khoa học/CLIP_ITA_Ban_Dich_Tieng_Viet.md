# Mở rộng CLIP cho Tác vụ Truy vấn Danh mục-sang-Hình ảnh trong Thương mại Điện tử
*(Extending CLIP for Category-to-image Retrieval in E-commerce)*

**Tác giả:** Mariya Hendriksen¹, Maurits Bleeker², Svitlana Vakulenko², Nanne van Noord², Ernst Kuiper³, Maarten de Rijke²  
¹ *AIRLab, Đại học Amsterdam*; ² *Đại học Amsterdam*; ³ *Bol.com*  
**Email:** m.hendriksen@uva.nl, m.j.r.bleeker@uva.nl, s.vakulenko@uva.nl, n.j.e.vannoord@uva.nl, ekuiper@bol.com, m.derijke@uva.nl  

---

## Tóm tắt (Abstract)
Thương mại điện tử cung cấp dữ liệu đa phương thức (*multimodal data*) phong phú nhưng ít khi được khai thác triệt để trong thực tế. Một khía cạnh của dữ liệu này là cây danh mục (*category tree*) được sử dụng trong tìm kiếm và gợi ý. Tuy nhiên, trong thực tế, trong suốt phiên làm việc của người dùng thường xảy ra sự bất tương thích giữa biểu diễn văn bản và biểu diễn hình ảnh của một danh mục cho trước. Xuất phát từ bài toán này, chúng tôi giới thiệu tác vụ truy vấn danh mục-sang-hình ảnh (*category-to-image retrieval*) trong thương mại điện tử và đề xuất mô hình cho tác vụ này, gọi là **CLIP-ITA**. Mô hình tận dụng thông tin từ nhiều phương thức (phương thức văn bản, hình ảnh và thuộc tính) để tạo ra các biểu diễn sản phẩm. Chúng tôi khám phá việc bổ sung thông tin từ nhiều phương thức ảnh hưởng thế nào đến hiệu năng của mô hình. Đặc biệt, chúng tôi quan sát thấy CLIP-ITA vượt trội đáng kể so với mô hình tương đương chỉ tận dụng phương thức hình ảnh và mô hình tương đương tận dụng phương thức hình ảnh cùng thuộc tính.

**Từ khóa:** Truy vấn đa phương thức (*Multimodal retrieval*) · Truy vấn danh mục-sang-hình ảnh (*Category-to-image retrieval*) · Thương mại điện tử (*E-commerce*)

---

## 1. Giới thiệu (Introduction)
Truy vấn đa phương thức là một bài toán lớn nhưng chưa được nghiên cứu đầy đủ trong thương mại điện tử [33]. Mặc dù các sản phẩm thương mại điện tử gắn liền với thông tin đa phương thức phong phú, nghiên cứu hiện tại chủ yếu tập trung vào tín hiệu văn bản và hành vi để hỗ trợ tìm kiếm và gợi ý sản phẩm. Phần lớn các công trình trước đây về truy vấn đa phương thức trong thương mại điện tử tập trung vào các ứng dụng trong lĩnh vực thời trang, chẳng hạn như gợi ý sản phẩm thời trang [21] và truy vấn thời trang xuyên phương thức (*cross-modal fashion retrieval*) [6, 14]. Trong lĩnh vực thương mại điện tử tổng quát hơn, truy vấn đa phương thức vẫn chưa được khám phá kỹ lưỡng [10, 18]. Bài toán đa phương thức mà chúng tôi tập trung được thúc đẩy bởi tầm quan trọng của thông tin danh mục trong thương mại điện tử. Cây danh mục sản phẩm là thành phần cốt lõi của thương mại điện tử hiện đại vì chúng hỗ trợ khách hàng điều hướng qua các danh mục sản phẩm lớn và biến động [13, 30, 36]. Tuy nhiên, khả năng truy vấn một hình ảnh cho một danh mục sản phẩm cho trước vẫn là một tác vụ thách thức, chủ yếu do dữ liệu danh mục và sản phẩm bị nhiễu, cùng với kích thước và tính chất biến động của danh mục sản phẩm [17, 33].

### Tác vụ truy vấn Danh mục-sang-Hình ảnh (Category-to-image retrieval task)
Chúng tôi giới thiệu bài toán truy vấn danh sách xếp hạng các hình ảnh liên quan của sản phẩm thuộc về một danh mục cho trước, gọi là tác vụ truy vấn danh mục-sang-hình ảnh (CtI). Không giống như các tác vụ phân loại hình ảnh hoạt động trên một tập hợp lớp cố định (*predefined set of classes*), trong tác vụ truy vấn CtI, chúng tôi muốn không chỉ hiểu hình ảnh nào thuộc về một danh mục cho trước mà còn có khả năng tổng quát hóa sang các danh mục chưa từng thấy (*unseen categories*). Hãy xét danh mục "Trang trí nhà cửa" (*Home decor*). Bài toán truy vấn CtI sẽ xuất ra một danh sách xếp hạng gồm $k$ hình ảnh được truy xuất từ tập hợp hình ảnh có liên quan đến danh mục, có thể là bất kỳ thứ gì từ hình ảnh thảm, hình ảnh đồng hồ hoặc sự sắp xếp các bình hoa trang trí. Các trường hợp sử dụng thúc đẩy tác vụ truy vấn CtI bao gồm:
1. Nhu cầu trưng bày các danh mục khác nhau trong kết quả tìm kiếm và gợi ý [13, 30, 33];
2. Tác vụ có thể dùng để suy luận danh mục sản phẩm trong trường hợp dữ liệu danh mục bị thiếu, nhiễu hoặc không đầy đủ [39];
3. Thiết kế các chương trình khuyến mãi chéo danh mục và trang đích danh mục sản phẩm (*landing pages*) [24].

Tác vụ truy vấn CtI có các đặc điểm chính:
1. Chúng tôi thao tác với các danh mục từ cây danh mục thương mại điện tử không cố định, trải dài từ rất tổng quát (như "Ô tô" - *Automotive* hoặc "Nhà cửa & Bếp" - *Home & Kitchen*) đến rất cụ thể (như "Lót mũ bảo hiểm" - *Helmet Liners* hoặc "Máy hút ẩm" - *Dehumidifiers*). Cây danh mục không cố định, do đó chúng tôi phải có khả năng tổng quát hóa sang các danh mục chưa từng thấy;
2. Thông tin sản phẩm mang bản chất đa phương thức cao; ngoài dữ liệu danh mục, sản phẩm có thể đi kèm với thông tin văn bản, hình ảnh và thuộc tính.

### Mô hình cho truy vấn CtI (A model for CtI retrieval)
Để giải quyết tác vụ truy vấn CtI, chúng tôi đề xuất một mô hình tận dụng thông tin hình ảnh, văn bản và thuộc tính, gọi là **CLIP-ITA**. CLIP-ITA mở rộng dựa trên mô hình Tiền huấn luyện Ngôn ngữ-Hình ảnh Tương phản (*Contrastive Language-Image Pre-Training* - CLIP) [26]. CLIP-ITA mở rộng CLIP với khả năng biểu diễn thông tin thuộc tính. Do đó, CLIP-ITA có khả năng sử dụng thông tin văn bản, hình ảnh và thuộc tính cho biểu diễn sản phẩm. Chúng tôi so sánh hiệu năng của CLIP-ITA với một số mô hình cơ sở (*baselines*) như BM25 đơn phương thức (*unimodal BM25*), zero-shot CLIP hai phương thức (*bimodal zero-shot CLIP*), và MPNet [29]. Cho các thực nghiệm, chúng tôi sử dụng tập dữ liệu XMarket chứa thông tin văn bản, hình ảnh và thuộc tính của các sản phẩm thương mại điện tử [2].

### Câu hỏi nghiên cứu và Đóng góp (Research questions and contributions)
Chúng tôi giải quyết các câu hỏi nghiên cứu sau:
- **(RQ1):** Các mô hình cơ sở (*baseline*) hoạt động như thế nào trên tác vụ truy vấn CtI? Cụ thể, các mô hình cơ sở đơn phương thức và hai phương thức đạt hiệu năng ra sao? Hiệu năng khác biệt như thế nào theo độ chi tiết của danh mục (*category granularity*)?
- **(RQ2):** Một mô hình, đặt tên là **CLIP-I**, sử dụng thông tin hình ảnh sản phẩm để xây dựng biểu diễn sản phẩm, tác động như thế nào đến hiệu năng trên tác vụ truy vấn CtI?
- **(RQ3):** **CLIP-IA**, mô hình mở rộng CLIP-I bằng thông tin thuộc tính sản phẩm, đạt hiệu năng như thế nào trên tác vụ truy vấn CtI?
- **(RQ4):** Và cuối cùng, **CLIP-ITA**, mô hình mở rộng CLIP-IA bằng thông tin văn bản sản phẩm, đạt hiệu năng như thế nào trên tác vụ CtI?

Các đóng góp chính của chúng tôi gồm:
1. Chúng tôi giới thiệu tác vụ mới truy vấn CtI và đưa ra động lực ứng dụng trong thương mại điện tử.
2. Chúng tôi đề xuất CLIP-ITA, mô hình đầu tiên được thiết kế chuyên biệt cho tác vụ này. CLIP-ITA tận dụng dữ liệu sản phẩm đa phương thức như văn bản, hình ảnh và thuộc tính. Trung bình, CLIP-ITA vượt trội hơn CLIP-I trên tất cả các danh mục là 217% và vượt CLIP-IA là 269%.
3. Chúng tôi chia sẻ mã nguồn và thiết lập thực nghiệm tại: `https://github.com/mariyahendriksen/ecir2022_category_to_image_retrieval`

---

## 2. Các công trình liên quan (Related Work)

### Học biểu diễn đa phương thức (Learning multimodal embeddings)
Huấn luyện tương phản (*Contrastive pre-training*) đã được chứng minh là rất hiệu quả trong việc học không gian biểu diễn chung giữa các phương thức [26]. Bằng cách dự đoán sự ghép cặp chính xác của bộ hai hình ảnh-văn bản trong một batch, mô hình CLIP có thể học các bộ mã hóa văn bản và hình ảnh mạnh mẽ chiếu vào một không gian chung. Cách tiếp cận học biểu diễn đa phương thức này mang lại các ưu điểm chính so với các cách tiếp cận dùng nhãn gán thủ công làm giám sát:
1. Dữ liệu huấn luyện có thể thu thập mà không cần gán nhãn thủ công; dữ liệu thế giới thực chứa các cặp hình ảnh-văn bản có thể được sử dụng trực tiếp;
2. Các mô hình được huấn luyện theo cách này học được biểu diễn tổng quát hơn, cho phép dự đoán zero-shot.

Những ưu điểm này rất hấp dẫn đối với thương mại điện tử, vì hầu hết các tập dữ liệu thương mại điện tử đa phương thức công khai chủ yếu tập trung vào thời trang [2]; việc có thể huấn luyện từ dữ liệu thế giới thực giúp tránh nhu cầu gán nhãn dữ liệu tốn kém. Chúng tôi phát triển dựa trên CLIP bằng cách mở rộng nó sang các cặp danh mục-sản phẩm, tận dụng khả năng thực hiện truy vấn zero-shot cho đa dạng các khái niệm ngữ nghĩa.

### Truy vấn hình ảnh đa phương thức (Multimodal image retrieval)
Các công trình ban đầu trong truy vấn hình ảnh nhóm các hình ảnh vào một tập hợp cố định các danh mục ngữ nghĩa và cho phép người dùng truy xuất hình ảnh bằng các nhãn danh mục làm câu truy vấn [28]. Các công trình sau đó cho phép đa dạng câu truy vấn hơn, từ ngôn ngữ tự nhiên [11, 34], thuộc tính [23], đến sự kết hợp của nhiều phương thức (ví dụ: tiêu đề, mô tả và thẻ) [32]. Trong các cách tiếp cận truy vấn hình ảnh đa phương thức này, chúng tôi tìm thấy ba thành phần chung:
1. Bộ mã hóa hình ảnh (*image encoder*);
2. Bộ mã hóa truy vấn (*query encoder*);
3. Hàm độ tương đồng (*similarity function*) để khớp câu truy vấn với hình ảnh [7, 26].

Tùy thuộc vào trọng tâm của công trình, một số thành phần có thể được tiền huấn luyện, trong khi các thành phần khác được tối ưu hóa cho tác vụ cụ thể. Trong công trình của chúng tôi, chúng tôi dựa vào bộ mã hóa hình ảnh và văn bản đã tiền huấn luyện nhưng học một biểu diễn tổng hợp đa phương thức mới của câu truy vấn để thực hiện truy vấn CtI.

### Truy vấn đa phương thức trong thương mại điện tử (Multimodal retrieval in e-commerce)
Các công trình trước đây về truy vấn đa phương thức trong thương mại điện tử chủ yếu tập trung vào truy vấn xuyên phương thức cho thời trang [6, 16, 42]. Các ví dụ liên quan khác bao gồm gợi ý trang phục [15, 19, 21]. Một số công trình trước đây về tính diễn giải cho truy vấn sản phẩm thời trang đề xuất tận dụng các tín hiệu đa phương thức để cải thiện khả năng giải thích của các đặc trưng ẩn [20, 38]. Tautkute et al. [31] đề xuất một công cụ tìm kiếm đa phương thức cho các mặt hàng thời trang và nội thất. Khi kết hợp các tín hiệu để cải thiện truy vấn sản phẩm, Yim et al. [40] đề xuất kết hợp hình ảnh, tiêu đề, danh mục và mô tả sản phẩm để cải thiện tìm kiếm sản phẩm. Yamaura et al. [37] đề xuất thuật toán tận dụng thông tin sản phẩm đa phương thức để dự đoán giá bán lại của sản phẩm đồ cũ. Khác với các công trình trước đây chủ yếu tập trung vào dữ liệu thời trang, chúng tôi tập trung vào việc tạo ra biểu diễn sản phẩm đa phương thức cho lĩnh vực thương mại điện tử tổng quát.

---

## 3. Phương pháp (Approach)

### Định nghĩa tác vụ (Task definition)
Chúng tôi sử dụng ký hiệu tương tự như trong [41]. Tập dữ liệu đầu vào có thể biểu diễn dưới dạng các cặp danh mục-sản phẩm $(x_c, x_p)$, trong đó $x_c$ đại diện cho danh mục sản phẩm, và $x_p$ đại diện cho thông tin về sản phẩm thuộc danh mục $x_c$. Danh mục sản phẩm $x_c$ được lấy từ cây danh mục $\mathcal{T}$ và được biểu diễn dưới dạng tên danh mục. Thông tin sản phẩm bao gồm tiêu đề $x_t$, hình ảnh $x_i$, và các thuộc tính $x_a$, tức là $x_p = \{x_i, x_t, x_a\}$. Đối với tác vụ truy vấn CtI, chúng tôi sử dụng tên danh mục mục tiêu $x_c$ làm câu truy vấn và hướng tới trả về một danh sách xếp hạng top-$k$ hình ảnh thuộc về danh mục $x_c$.

### Kiến trúc CLIP-ITA (CLIP-ITA Architecture)
CLIP-ITA chiếu danh mục $x_c$ và thông tin sản phẩm $x_p$ vào không gian đa phương thức $d$-chiều, nơi các vectơ kết quả tương ứng là $c$ và $p$. Thông tin danh mục và sản phẩm được xử lý bởi luồng mã hóa danh mục (*category encoding pipeline*) và luồng mã hóa thông tin sản phẩm (*product information encoding pipeline*). Các thành phần cốt lõi của CLIP-ITA là các mô-đun mã hóa và chiếu (*projection modules*). Mô hình bao gồm bốn bộ mã hóa: bộ mã hóa danh mục (*category encoder*), bộ mã hóa hình ảnh (*image encoder*), bộ mã hóa tiêu đề (*title encoder*), và bộ mã hóa thuộc tính (*attribute encoder*). Ngoài ra, CLIP-ITA bao gồm hai đầu chiếu phi tuyến (*non-linear projection heads*): đầu chiếu danh mục (*category projection head*) và đầu chiếu đa phương thức (*multimodal projection head*).

Mặc dù một số thành phần của CLIP-ITA dựa trên CLIP [26], CLIP-ITA khác với CLIP theo ba điểm quan trọng:
1. Không giống như CLIP chỉ hoạt động trên hai bộ mã hóa (văn bản và hình ảnh), CLIP-ITA mở rộng CLIP thành bộ mã hóa danh mục, bộ mã hóa hình ảnh, bộ mã hóa văn bản và bộ mã hóa thuộc tính;
2. CLIP-ITA sở hữu hai đầu chiếu: một cho luồng mã hóa danh mục và một cho luồng mã hóa thông tin sản phẩm;
3. Trong khi CLIP được huấn luyện trên các cặp văn bản-hình ảnh, CLIP-ITA được huấn luyện trên các cặp danh mục-sản phẩm, trong đó biểu diễn sản phẩm là đa phương thức.

#### Luồng mã hóa danh mục (Category encoding pipeline)
Bộ mã hóa danh mục ($f_c$) nhận đầu vào là tên danh mục $x_c$ và trả về biểu diễn $h_c$:
$$h_c = f_c(x_c) \quad (1)$$
Để thu được biểu diễn này, chúng tôi sử dụng mô hình MPNet tiền huấn luyện [29]. Sau khi truyền thông tin danh mục qua bộ mã hóa danh mục, chúng tôi đưa nó vào đầu chiếu danh mục ($g_c$). Đầu chiếu danh mục $g_c$ nhận đầu vào là biểu diễn câu truy vấn $h_c$ và chiếu nó vào không gian đa phương thức $d$-chiều:
$$c = g_c(h_c) \quad (2)$$
trong đó $c \in \mathbb{R}^d$.

#### Luồng mã hóa sản phẩm (Product encoding pipeline)
Luồng mã hóa thông tin sản phẩm bao gồm ba bộ mã hóa, một cho mỗi phương thức, và một đầu chiếu sản phẩm:
- **Bộ mã hóa hình ảnh ($f_i$):** nhận đầu vào là hình ảnh sản phẩm $x_i$ căn chỉnh với danh mục $x_c$:
$$h_i = f_i(x_i) \quad (3)$$
Để thu được biểu diễn hình ảnh $h_i$, chúng tôi sử dụng Vision Transformer (ViT) tiền huấn luyện từ mô hình CLIP.
- **Bộ mã hóa tiêu đề ($f_t$):** nhận tiêu đề sản phẩm $x_t$ làm đầu vào và trả về biểu diễn tiêu đề $h_t$:
$$h_t = f_t(x_t) \quad (4)$$
Tương tự bộ mã hóa danh mục $f_c$, chúng tôi sử dụng MPNet tiền huấn luyện để thu được biểu diễn tiêu đề $h_t$.
- **Bộ mã hóa thuộc tính ($f_a$):** là một mạng nhận đầu vào là tập hợp các thuộc tính $x_a = \{a_1, a_2, \dots, a_n\}$ và trả về biểu diễn chung của chúng:
$$h_a = f_a(x_a) = \frac{1}{n} \sum_{i=1}^n f_a(x_{a,i}) \quad (5)$$
Tương tự bộ mã hóa danh mục $f_c$ và bộ mã hóa tiêu đề $f_t$, chúng tôi thu được biểu diễn của từng thuộc tính bằng mô hình MPNet tiền huấn luyện.

Sau khi thu được các biểu diễn tiêu đề, hình ảnh và thuộc tính, chúng tôi đưa các biểu diễn này vào đầu chiếu sản phẩm ($g_p$). Đầu chiếu sản phẩm $g_p$ nhận đầu vào là chuỗi nối (*concatenation*) của biểu diễn hình ảnh $h_i$, biểu diễn tiêu đề $h_t$, và biểu diễn thuộc tính $h_a$, rồi chiếu vectơ kết quả $h_p = \text{concat}(h_i, h_t, h_a)$ vào không gian đa phương thức:
$$p = g_p(h_p) = g_p(\text{concat}(h_i, h_t, h_a)) \quad (6)$$
trong đó $p \in \mathbb{R}^d$.

#### Hàm mất mát (Loss function)
Chúng tôi huấn luyện CLIP-ITA bằng hàm mất mát tương phản hai chiều (*bidirectional contrastive loss*) [41]. Hàm mất mát là sự kết hợp có trọng số của hai hàm mất mát: mất mát tương phản danh mục-sang-sản phẩm (*category-to-product contrastive loss*) và mất mát tương phản sản phẩm-sang-danh mục (*product-to-category contrastive loss*). Trong cả hai trường hợp, hàm mất mát đều là InfoNCE loss [25]. Không giống các công trình trước đây tập trung vào mất mát tương phản giữa các đầu vào cùng phương thức [3, 8] hoặc các đầu vào tương ứng của hai phương thức [41], chúng tôi sử dụng hàm mất mát để làm việc với đầu vào từ phương thức văn bản (biểu diễn danh mục) so với sự kết hợp của nhiều phương thức (biểu diễn sản phẩm).

Chúng tôi huấn luyện CLIP-ITA trên các batch chứa các cặp danh mục-sản phẩm $(x_c, x_p)$ với kích thước batch $\beta$. Đối với cặp thứ $j$ trong batch, mất mát tương phản danh mục-sang-sản phẩm được tính như sau:
$$\ell_j^{(c \to p)} = -\log \frac{\exp(f_{\text{sim}}(c_j, p_j) / \tau)}{\sum_{k=1}^\beta \exp(f_{\text{sim}}(c_j, p_k) / \tau)} \quad (7)$$
trong đó $f_{\text{sim}}(c_i, p_i)$ là độ tương đồng cosine (*cosine similarity*), và $\tau \in \mathbb{R}^+$ là tham số nhiệt độ (*temperature parameter*).

Tương tự, mất mát tương phản sản phẩm-sang-danh mục được tính như sau:
$$\ell_j^{(p \to c)} = -\log \frac{\exp(f_{\text{sim}}(p_j, c_j) / \tau)}{\sum_{k=1}^\beta \exp(f_{\text{sim}}(p_j, c_k) / \tau)} \quad (8)$$

Hàm mất mát tương phản tổng hợp là sự kết hợp của hai hàm mất mát nêu trên:
$$\mathcal{L} = \frac{1}{\beta} \sum_{j=1}^\beta \left( \lambda \ell_j^{(p \to c)} + (1 - \lambda) \ell_j^{(c \to p)} \right) \quad (9)$$
trong đó $\beta$ đại diện cho kích thước batch và $\lambda \in [0, 1]$ là trọng số vô hướng (*scalar weight*).

---

## 4. Thiết lập thực nghiệm (Experimental Setup)

### Tập dữ liệu (Dataset)
Chúng tôi sử dụng tập dữ liệu XMarket mới được giới thiệu bởi Bonab et al. [2] chứa thông tin văn bản, hình ảnh và thuộc tính của các sản phẩm thương mại điện tử cũng như cây danh mục. Cho các thực nghiệm, chúng tôi chọn 38,921 sản phẩm từ thị trường Mỹ (US market). Thông tin danh mục được biểu diễn dạng cây danh mục và bao gồm 5,471 danh mục duy nhất trải dài qua 9 cấp độ. Cấp 1 là cấp danh mục tổng quát nhất, cấp 9 là cấp cụ thể nhất. Mỗi sản phẩm thuộc về một cây con các danh mục $t \in \mathcal{T}$. Trong mỗi cây con $t$, mỗi danh mục cha chỉ có một danh mục con tương ứng. Độ sâu trung bình của cây con là 4.63 (tối thiểu: 2, tối đa: 9). Vì mỗi sản phẩm thuộc về một cây con danh mục, tập dữ liệu chứa tổng cộng 180,094 cặp sản phẩm-danh mục. Chúng tôi sử dụng tiêu đề sản phẩm làm thông tin văn bản và một hình ảnh cho mỗi sản phẩm làm thông tin hình ảnh. Thông tin thuộc tính bao gồm 228,368 thuộc tính, với 157,049 thuộc tính duy nhất. Trung bình mỗi sản phẩm có 5.87 thuộc tính (tối thiểu: 1, tối đa: 24).

### Phương pháp đánh giá (Evaluation method)
Để nghiên cứu hiệu năng mô hình thay đổi ra sao theo độ chi tiết danh mục, đối với mỗi sản phẩm $x_p$ trong tập dữ liệu và cây con danh mục tương ứng $t$, chúng tôi huấn luyện và đánh giá hiệu năng mô hình trong ba thiết lập:
1. **Tất cả danh mục (*All categories*):** chọn ngẫu nhiên một danh mục từ cây con $t$ (tổng cộng 5,471 danh mục);
2. **Danh mục tổng quát nhất (*Most general category*):** chỉ sử dụng danh mục tổng quát nhất của cây con $t$, tức là danh mục gốc (*root*) (tổng cộng 34 danh mục);
3. **Danh mục cụ thể nhất (*Most specific category*):** sử dụng danh mục cụ thể nhất của cây con $t$ (tổng cộng 4,100 danh mục).

Chúng tôi đánh giá mọi mô hình trên các cặp danh mục-sản phẩm $(x_c, x_p)$ từ tập kiểm thử (*test set*). Chúng tôi mã hóa từng danh mục và dữ liệu sản phẩm ứng viên bằng cách truyền qua luồng mã hóa danh mục và luồng mã hóa thông tin sản phẩm. Đối với mỗi danh mục $x_c$, chúng tôi truy xuất top-$k$ ứng viên xếp hạng theo độ tương đồng cosine so với danh mục mục tiêu $x_c$.

### Độ đo đánh giá (Metrics)
Để đánh giá hiệu năng mô hình, chúng tôi sử dụng Precision@K với $K \in \{1, 5, 10\}$, mAP@K với $K \in \{5, 10\}$, và R-precision.

### Các mô hình cơ sở (Baselines)
Theo [4, 27, 35], chúng tôi sử dụng BM25, MPNet, CLIP làm mô hình cơ sở.

### Bốn thực nghiệm (Four experiments)
Chúng tôi thực hiện bốn thực nghiệm tương ứng với các câu hỏi nghiên cứu ở Phần 1:
- **Thực nghiệm 1:** Đánh giá các mô hình cơ sở trên tác vụ truy vấn CtI (RQ1). Đưa vào tập văn bản BM25 thông tin văn bản sản phẩm (tiêu đề). Sử dụng MPNet theo cách zero-shot. Đối với tất cả sản phẩm, truyền tiêu đề $x_t$ qua MPNet. Khi đánh giá, truyền danh mục $x_c$ (dưới dạng truy vấn văn bản) qua MPNet và truy xuất top-$k$ ứng viên xếp hạng theo độ tương đồng cosine. So sánh danh mục của ứng viên với danh mục mục tiêu. Dùng CLIP tiền huấn luyện zero-shot với Text Transformer và Vision Transformer (ViT). Truyền hình ảnh $x_i$ qua bộ mã hóa hình ảnh. Khi đánh giá, truyền danh mục $x_c$ qua bộ mã hóa văn bản và truy xuất top-$k$ ứng viên hình ảnh.
- **Thực nghiệm 2:** Đánh giá biểu diễn sản phẩm dựa trên hình ảnh (RQ2). Sau khi có kết quả zero-shot của CLIP, chúng tôi xây dựng biểu diễn sản phẩm bằng cách huấn luyện trên dữ liệu thương mại điện tử. Để đưa vào thông tin hình ảnh, mở rộng CLIP theo hai cách: (1) Dùng ViT từ CLIP làm bộ mã hóa hình ảnh $f_i$, thêm đầu chiếu sản phẩm $g_p$ nhận đầu vào là thông tin hình ảnh $x_i \in x_p$; (2) Dùng bộ mã hóa văn bản từ MPNet làm bộ mã hóa danh mục $f_c$, thêm đầu chiếu danh mục $g_c$ lên trên $f_c$. Mô hình kết quả đặt tên là **CLIP-I** (chỉ dùng $x_p = \{x_i\}$).
- **Thực nghiệm 3:** Đánh giá biểu diễn dựa trên hình ảnh và thuộc tính (RQ3). Mở rộng CLIP-I bằng cách đưa thông tin thuộc tính vào luồng mã hóa thông tin sản phẩm. Thêm bộ mã hóa thuộc tính $f_a$ để thu được biểu diễn $h_a$. Nối biểu diễn thuộc tính với hình ảnh $h_p = \text{concat}(h_i, h_a)$ và đưa vào đầu chiếu $g_p$. Mô hình kết quả đặt tên là **CLIP-IA** (dùng $x_p = \{x_i, x_a\}$).
- **Thực nghiệm 4:** Đánh giá biểu diễn dựa trên hình ảnh, thuộc tính và tiêu đề (RQ4). Mở rộng luồng xử lý với phương thức văn bản (tiêu đề sản phẩm). Thêm bộ mã hóa tiêu đề $f_t$ để thu được $h_t$. Nối biểu diễn tiêu đề với hình ảnh và thuộc tính $h_p = \text{concat}(h_i, h_t, h_a)$ và đưa vào đầu chiếu $g_p$. Mô hình kết quả là **CLIP-ITA** (dùng $x_p = \{x_i, x_a, x_t\}$).

### Chi tiết cài đặt (Implementation details)
Huấn luyện mỗi mô hình trong 30 epochs, kích thước batch $\beta = 8$ cho danh mục tổng quát nhất, $\beta = 128$ cho danh mục cụ thể nhất và tất cả danh mục. Hàm mất mát cài đặt $\tau = 1, \lambda = 0.5$. Các đầu chiếu là MLP phi tuyến với 2 lớp ẩn, kích hoạt GELU và Layer Normalization. Tối ưu hóa bằng AdamW.

---

## 5. Kết quả thực nghiệm (Experimental Results)

### Bảng 1: Kết quả các thực nghiệm 1–4
*(Giá trị tốt nhất trong từng phần được bôi đậm)*

| Mô hình | P@1 | P@5 | P@10 | MAP@5 | MAP@10 | R-precision |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tất cả danh mục (5,471)** | | | | | | |
| BM25 [12] | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| CLIP [26] | 0.01 | 0.02 | 0.02 | 0.03 | 0.04 | 0.02 |
| MPNet [29] | 0.01 | 0.06 | 0.06 | 0.07 | 0.09 | 0.05 |
| CLIP-I (Ours) | 3.30 | 3.80 | 3.79 | 6.81 | 7.25 | 3.67 |
| CLIP-IA (Ours) | 2.50 | 3.34 | 3.29 | 5.95 | 6.24 | 3.27 |
| **CLIP-ITA (Ours)** | **9.90** | **13.27** | **13.43** | **20.30** | **20.53** | **13.42** |
| **Danh mục tổng quát nhất (34)** | | | | | | |
| BM25 [12] | 2.94 | 4.71 | 4.71 | 8.33 | 8.28 | 4.48 |
| CLIP [26] | 11.76 | 12.35 | 11.76 | 16.12 | 15.18 | 9.47 |
| MPNet [29] | 14.70 | 15.80 | 15.01 | 18.44 | 18.78 | 9.35 |
| CLIP-I (Ours) | 17.85 | 17.14 | 16.78 | 19.88 | 20.14 | 13.02 |
| CLIP-IA (Ours) | 21.42 | 21.91 | 22.78 | 25.59 | 26.29 | 20.74 |
| **CLIP-ITA (Ours)** | **35.71** | **30.95** | **30.95** | **35.51** | **34.28** | **25.79** |
| **Danh mục cụ thể nhất (4,100)** | | | | | | |
| BM25 [12] | 0.02 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 |
| CLIP [26] | 11.92 | 9.81 | 9.23 | 15.12 | 14.95 | 8.14 |
| MPNet [29] | 33.36 | 28.56 | 26.93 | 37.43 | 36.77 | 25.29 |
| CLIP-I (Ours) | 14.06 | 12.11 | 11.53 | 18.24 | 17.90 | 11.22 |
| CLIP-IA (Ours) | 35.30 | 30.21 | 29.32 | 39.93 | 39.27 | 28.86 |
| **CLIP-ITA (Ours)** | **45.85** | **41.04** | **40.02** | **50.04** | **49.87** | **39.69** |

### Phân tích chi tiết từng thực nghiệm

- **Thực nghiệm 1: Các mô hình cơ sở (Baselines - RQ1):**
  Khi đánh giá trên tất cả danh mục, tất cả các mô hình cơ sở đều thể hiện kém. Ở thiết lập danh mục tổng quát nhất, MPNet vượt CLIP ở hầu hết các chỉ số trừ R-precision (Precision@10 cao hơn 28%). CLIP vượt BM25 trên mọi chỉ số. Ở danh mục cụ thể nhất, MPNet đạt hiệu năng cao nhất (vượt CLIP 211% ở Precision@10). Nhìn chung, kết quả khẳng định việc tận dụng thông tin đa phương thức mang lại lợi ích rõ rệt cho tác vụ CtI.

- **Thực nghiệm 2: Biểu diễn sản phẩm dựa trên hình ảnh (Image-based - RQ2):**
  CLIP-I vượt qua CLIP trong cả 3 thiết lập và vượt MPNet ngoại trừ ở danh mục cụ thể nhất. Ở danh mục tổng quát nhất, CLIP-I vượt CLIP 51% ở Precision@1 và vượt MPNet 39% ở R-precision. Kết quả cho thấy việc mở rộng CLIP bằng cách đưa dữ liệu hình ảnh sản phẩm để xây dựng biểu diễn sản phẩm có tác động tích cực đến hiệu năng truy vấn CtI.

- **Thực nghiệm 3: Biểu diễn sản phẩm dựa trên hình ảnh và thuộc tính (Image- and Attribute-based - RQ3):**
  Ở danh mục tổng quát nhất và cụ thể nhất, CLIP-IA vượt trội hơn CLIP-I và MPNet trên mọi chỉ số (đạt mức tăng tương đối lớn nhất 138% ở danh mục cụ thể nhất so với CLIP-I). Điều này khẳng định việc tích hợp thuộc tính sản phẩm giúp mô hình phân biệt tốt hơn các danh mục mang tính chi tiết.

- **Thực nghiệm 4: Biểu diễn sản phẩm kết hợp hình ảnh, thuộc tính và tiêu đề (Image-, Attribute-, and Title-based - RQ4):**
  CLIP-ITA giành chiến thắng áp đảo trong cả 3 thiết lập. Trên tất cả danh mục, CLIP-ITA tăng tối đa 265% R-precision so với CLIP-I và 310% Precision@1 so với CLIP-IA. Ở danh mục tổng quát nhất, CLIP-ITA vượt CLIP-I 82% và CLIP-IA 38%. Ở danh mục cụ thể nhất, CLIP-ITA vượt CLIP-I 254% ở R-precision. Kết quả khẳng định việc kết hợp cả 3 phương thức đem lại biểu diễn tối ưu nhất cho truy vấn CtI.

---

## 6. Phân tích lỗi (Error Analysis)

### Khoảng cách giữa danh mục dự đoán và danh mục mục tiêu (Distance between predicted and target categories)
Chúng tôi kiểm tra các cặp danh mục thực tế và danh mục dự đoán $(c, c_p)$ khi mô hình dự đoán sai ($c \neq c_p$).

### Bảng 2: Số lượng dự đoán sai của CLIP-ITA thuộc "cùng cây" vs. "khác cây" danh mục

| Loại đánh giá | Cùng cây (*Same tree*) | Khác cây (*Different tree*) |
| :--- | :---: | :---: |
| Tất cả danh mục (*All categories*) | 1,655 | 639 |
| Danh mục tổng quát nhất (*Most general category*) | 2 | 21 |
| Danh mục cụ thể nhất (*Most specific category*) | 127 | 1,011 |
| **Tổng cộng** | **1,786** | **1,671** |

Khoảng cách được tính bằng sự khác biệt về độ sâu $d(c, c_p) = \text{depth}(c_p) - \text{depth}(c)$:
- Đối với danh mục cụ thể nhất, các danh mục dự đoán sai trong cùng cây đều có độ sâu nhỏ hơn danh mục mục tiêu ($d < 0$). Trong 68% trường hợp, danh mục dự đoán nằm ngay trên danh mục mục tiêu 1 cấp ($d = -1$).
- Đối với thiết lập tất cả danh mục, trong 92% trường hợp dự đoán sai cùng cây, danh mục dự đoán cụ thể hơn danh mục mục tiêu ($d > 0$).
- Phân tích gợi ý rằng các nỗ lực cải tiến CLIP-ITA nên tập trung vào việc giảm thiểu khoảng cách trên cây danh mục giữa danh mục mục tiêu và danh mục dự đoán, có thể thông qua việc tích hợp cấu trúc cây vào hàm mất mát.

### Hiệu năng trên danh mục đã thấy vs. chưa thấy (Performance on seen vs. unseen categories)

### Bảng 3: Hiệu năng CLIP-ITA trên các danh mục đã thấy (seen) vs. chưa thấy (unseen)

| Mô hình / Thiết lập | P@1 | P@5 | P@10 | mAP@5 | mAP@10 | R-precision |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tất cả danh mục (5,471)** | | | | | | |
| CLIP-ITA (danh mục chưa thấy - *unseen*) | 13.30 | 18.56 | 15.55 | 19.70 | 19.65 | 18.52 |
| CLIP-ITA (danh mục đã thấy - *seen*) | 10.48 | 13.95 | 14.08 | 21.65 | 21.65 | 14.07 |
| **Danh mục tổng quát nhất (34)** | | | | | | |
| CLIP-ITA (danh mục chưa thấy - *unseen*) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| CLIP-ITA (danh mục đã thấy - *seen*) | 19.23 | 20.01 | 17.31 | 20.41 | 20.01 | 15.73 |
| **Danh mục cụ thể nhất (4,100)** | | | | | | |
| CLIP-ITA (danh mục chưa thấy - *unseen*) | 27.27 | 26.44 | 26.44 | 27.92 | 27.92 | 26.45 |
| CLIP-ITA (danh mục đã thấy - *seen*) | 47.83 | 43.09 | 42.14 | 52.41 | 51.89 | 41.58 |

Nhìn chung:
- Ở danh mục tổng quát nhất và cụ thể nhất, mô hình đạt hiệu năng tốt hơn rõ rệt trên các danh mục đã xuất hiện trong quá trình huấn luyện (*seen categories*).
- Ở thiết lập tất cả danh mục, CLIP-ITA thể hiện khả năng tổng quát hóa ấn tượng khi đạt điểm số cao hơn trên các danh mục chưa từng thấy (*unseen categories*) đối với các chỉ số Precision@k và R-precision.

---

## 7. Kết luận (Conclusion)
Chúng tôi đã giới thiệu tác vụ truy vấn danh mục-sang-hình ảnh (CtI) và làm rõ tầm quan trọng của tác vụ này trong ngữ cảnh thương mại điện tử. Chúng tôi đề xuất CLIP-ITA - mô hình đầu tiên được thiết kế chuyên biệt cho tác vụ CtI, mở rộng từ mô hình CLIP. CLIP-ITA kết hợp thông tin đa phương thức (văn bản tiêu đề, hình ảnh và thuộc tính sản phẩm) để xây dựng biểu diễn sản phẩm phong phú. Các thực nghiệm cho thấy việc kết hợp cả 3 phương thức đem lại kết quả vượt trội trên toàn bộ các thiết lập danh mục.

### Hạn chế và Hướng nghiên cứu tương lai (Limitations & Future Work)
- **Hạn chế:** Do đặc thù của dữ liệu thương mại điện tử (thường chỉ có 1 đối tượng/ảnh trên phông nền đơn sắc, văn bản tiêu đề dài và chứa nhiều nhiễu), khác với dữ liệu ảnh tự nhiên tổng quát.
- **Hướng tương lai:**
  1. Tích hợp cơ chế chú ý (*attention mechanisms*) vào bộ mã hóa thuộc tính;
  2. Đánh giá CLIP-ITA trên các tập dữ liệu đa dạng ngoài lĩnh vực thương mại điện tử;
  3. Bổ sung các hàm mất mát nhằm giảm thiểu khoảng cách phân cấp cây giữa danh mục mục tiêu và danh mục dự đoán.

---

## Lời cảm ơn (Acknowledgements)
Nghiên cứu này được hỗ trợ bởi Ahold Delhaize, Nationale Politie, và Trung tâm Trí tuệ Hỗn hợp (Hybrid Intelligence Center) - chương trình 10 năm được tài trợ bởi Bộ Giáo dục, Văn hóa và Khoa học Hà Lan thông qua Tổ chức Nghiên cứu Khoa học Hà Lan (NWO), `https://hybrid-intelligence-centre.nl`. Tất cả nội dung thể hiện quan điểm của các tác giả và không nhất thiết đại diện cho nhà tuyển dụng hoặc nhà tài trợ.

---

## Tài liệu tham khảo (Bibliography)
[1] Ba JL, Kiros JR, Hinton GE (2016) Layer normalization. arXiv preprint arXiv:1607.06450  
[2] Bonab H, Aliannejadi M, Vardasbi A, Kanoulas E, Allan J (2021) XMarket: Cross-market training for product recommendation. In: CIKM, ACM  
[3] Chen T, Kornblith S, Norouzi M, Hinton G (2020) A simple framework for contrastive learning of visual representations. In: ICML, PMLR, pp 1597–1607  
[4] Dai Z, Lai G, Yang Y, Le QV (2020) Funnel-transformer: Filtering out sequential redundancy for efficient language processing. arXiv:2006.03236  
[5] Dosovitskiy A, Beyer L, Kolesnikov A, Weissenborn D, Zhai X, Unterthiner T, Dehghani M, Minderer M, Heigold G, Gelly S, Uszkoreit J, Houlsby N (2021) An image is worth 16x16 words: Transformers for image recognition at scale. In: ICLR  
[6] Goei K, Hendriksen M, de Rijke M (2021) Tackling attribute finegrainedness in cross-modal fashion search with multi-level features. In: SIGIR Workshop on eCommerce  
[7] Gupta T, Vahdat A, Chechik G, Yang X, Kautz J, Hoiem D (2020) Contrastive learning for weakly supervised phrase grounding. In: ECCV  
[8] He K, Fan H, Wu Y, Xie S, Girshick R (2020) Momentum contrast for unsupervised visual representation learning. In: CVPR, pp 9729–9738  
[9] Hendrycks D, Gimpel K (2016) Gaussian error linear units (GELUs). arXiv preprint arXiv:1606.08415  
[10] Hewawalpita S, Perera I (2019) Multimodal user interaction framework for e-commerce. In: IRC SCSE, IEEE, pp 9–16  
[11] Hu R, Xu H, Rohrbach M, Feng J, Saenko K, Darrell T (2016) Natural language object retrieval. In: CVPR, pp 4555–4564  
[12] Jones KS, Walker S, Robertson SE (2000) A probabilistic model of information retrieval: development and comparative experiments: Part 2. IP&M 36(6):809–840  
[13] Kondylidis N, Zou J, Kanoulas E (2021) Category aware explainable conversational recommendation. arXiv preprint arXiv:2103.08733  
[14] Laenen K, Moens MF (2019) Multimodal neural machine translation of fashion e-commerce descriptions. In: Fashion Communication, Springer  
[15] Laenen K, Moens MF (2020) A comparative study of outfit recommendation methods with a focus on attention-based fusion. IP&M 57(6):102316  
[16] Laenen K, Zoghbi S, Moens MF (2017) Cross-modal search for fashion attributes. In: KDD Workshop on ML Meets Fashion  
[17] Laenen K, Zoghbi S, Moens MF (2018) Web search of fashion items with multimodal querying. In: WSDM, pp 342–350  
[18] Li H, Yuan P, Xu S, Wu Y, He X, Zhou B (2020) Aspect-aware multimodal summarization for chinese e-commerce products. In: AAAI 34:8188–8195  
[19] Li X, Wang X, He X, Chen L, Xiao J, Chua TS (2020) Hierarchical fashion graph network for personalized outfit recommendation. In: SIGIR, pp 159–168  
[20] Liao L, He X, Zhao B, Ngo CW, Chua TS (2018) Interpretable multimodal retrieval for fashion products. In: ACM MM, pp 1571–1579  
[21] Lin Y, Ren P, Chen Z, Ren Z, Ma J, de Rijke M (2019) Improving outfit recommendation with co-supervision of fashion generation. In: WWW, pp 1095–1105  
[22] Loshchilov I, Hutter F (2017) Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101  
[23] Nagarajan T, Grauman K (2018) Attributes as operators: factorizing unseen attribute-object compositions. In: ECCV, pp 169–185  
[24] Nielsen J, Molich R, Snyder C, Farrell S (2000) E-commerce user experience. Nielsen Norman Group  
[25] Oord Avd, Li Y, Vinyals O (2018) Representation learning with contrastive predictive coding. arXiv preprint arXiv:1807.03748  
[26] Radford A, Kim JW, Hallacy C, Ramesh A, Goh G, Agarwal S, Sastry G, Askell A, Mishkin P, Clark J, et al. (2021) Learning transferable visual models from natural language supervision. arXiv preprint arXiv:2103.00020  
[27] Shen S, Li LH, Tan H, Bansal M, Rohrbach A, Chang KW, Yao Z, Keutzer K (2021) How much can CLIP benefit vision-and-language tasks? arXiv:2107.06383  
[28] Smeulders A, Worring M, Santini S, Gupta A, Jain R (2000) Content-based image retrieval at the end of the early years. IEEE TPAMI 22(12):1349–1380  
[29] Song K, Tan X, Qin T, Lu J, Liu TY (2020) MPNet: Masked and permuted pre-training for language understanding. arXiv preprint arXiv:2004.09297  
[30] Tagliabue J, Yu B, Beaulieu M (2020) How to grow a (product) tree: personalized category suggestions for ecommerce type-ahead. arXiv:2005.12781  
[31] Tautkute I, Trzciński T, Skorupa AP, Brocki L, Marasek K (2019) Deep-style: Multimodal search engine for fashion and interior design. IEEE Access 7:84613–84628  
[32] Thomee B, Shamma DA, Friedland G, Elizalde B, Ni K, Poland D, Borth D, Li LJ (2016) YFCC100M: The new data in multimedia research. CACM 59(2):64–73  
[33] Tsagkias M, King TH, Kallumadi S, Murdock V, de Rijke M (2020) Challenges and research opportunities in ecommerce search and recommendations. SIGIR Forum 54(1)  
[34] Vo N, Jiang L, Sun C, Murphy K, Li LJ, Fei-Fei L, Hays J (2019) Composing text and image for image retrieval-an empirical odyssey. In: CVPR, pp 6439–6448  
[35] Wang S, Zhuang S, Zuccon G (2021) Bert-based dense retrievers require interpolation with bm25 for effective passage retrieval. In: ICTIR, pp 317–324  
[36] Wirojwatanakul P, Wangperawong A (2019) Multi-label product categorization using multi-modal fusion models. arXiv preprint arXiv:1907.00420  
[37] Yamaura Y, Kanemaki N, Tsuboshita Y (2019) The resale price prediction of secondhand jewelry items using a multi-modal deep model with iterative co-attention. arXiv:1907.00661  
[38] Yang X, He X, Wang X, Ma Y, Feng F, Wang M, Chua TS (2019) Interpretable fashion matching with rich attributes. In: SIGIR, pp 775–784  
[39] Yashima T, Okazaki N, Inui K, Yamaguchi K, Okatani T (2016) Learning to describe e-commerce images from noisy online data. In: ACCV, pp 85–100  
[40] Yim J, Kim JJ, Shin D (2018) One-shot item search with multimodal data. arXiv preprint arXiv:1811.10969  
[41] Zhang Y, Jiang H, Miura Y, Manning CD, Langlotz CP (2020) Contrastive learning of medical visual representations from paired images and text. arXiv:2010.00747  
[42] Zoghbi S, Heyman G, Gomez JC, Moens MF (2016) Cross-modal fashion search. In: MMM, Springer, pp 367–373  
