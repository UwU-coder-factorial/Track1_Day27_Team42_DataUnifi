# Tóm tắt dự án DataUnifi

> Project evidence note: this document records the confirmed DataUnifi project design and intended workflows. It does not claim production deployment, measured accuracy, user validation, or business impact.

## 1. Dự án là gì?

**DataUnifi** là một nền tảng web đa tenant (multi-tenant) ứng dụng AI để hỗ trợ doanh nghiệp **làm sạch, chuẩn hóa và ghép nối hồ sơ khách hàng** từ nhiều nguồn dữ liệu khác nhau.

Mỗi công ty, phòng ban hoặc đơn vị nghiệp vụ được xem là một tenant độc lập. Dữ liệu gốc của từng tenant được lưu và xử lý riêng; hệ thống không gom toàn bộ dữ liệu thật của các bên vào một kho dữ liệu chung. AI đóng vai trò đề xuất phương án xử lý, còn những quyết định quan trọng liên quan đến thay đổi hoặc chia sẻ dữ liệu vẫn được con người kiểm tra và phê duyệt.

Hai chức năng cốt lõi của dự án là:

1. **AI Data Cleaning:** phát hiện dữ liệu không nhất quán và đề xuất các rule làm sạch, chuẩn hóa.
2. **Entity Matching:** xác định các bản ghi ở nhiều nguồn có khả năng thuộc cùng một khách hàng mà vẫn kiểm soát quyền riêng tư.

## 2. Dự án dùng để làm gì?

Trong thực tế, dữ liệu khách hàng thường được lưu ở nhiều hệ thống và nhập theo nhiều cách khác nhau. Một người có thể xuất hiện dưới nhiều bản ghi do:

- Tên bị viết hoa/thường không thống nhất, thiếu dấu hoặc sai chính tả.
- Số điện thoại, CCCD và ngày sinh có định dạng khác nhau.
- Địa chỉ sử dụng tên cũ, tên viết tắt hoặc cách trình bày khác nhau.
- Các hệ thống sử dụng tên cột và cấu trúc dữ liệu không giống nhau.

Việc xử lý thủ công các vấn đề này tốn thời gian, dễ sai sót và khó mở rộng khi dữ liệu lớn. Đồng thời, nếu chia sẻ trực tiếp dữ liệu giữa nhiều công ty hoặc phòng ban thì có nguy cơ làm lộ thông tin cá nhân và dữ liệu nhạy cảm.

DataUnifi được xây dựng nhằm:

- Giảm thời gian làm sạch và chuẩn hóa dữ liệu thủ công.
- Nâng cao chất lượng dữ liệu trước khi phân tích hoặc đối soát.
- Nhận diện cùng một khách hàng đang xuất hiện ở những nguồn nào.
- Hỗ trợ cộng tác giữa nhiều đơn vị mà không công khai toàn bộ dữ liệu gốc.
- Đảm bảo thao tác truy cập, phê duyệt và xuất dữ liệu đều có thể truy vết.
- Hạn chế ghép nhầm hồ sơ bằng cơ chế chấm điểm, vùng cần review và phê duyệt của con người.

DataUnifi không nhằm thay thế CRM/ERP hiện có và cũng không tự động xây dựng một hồ sơ khách hàng hợp nhất duy nhất. Hệ thống hoạt động như một lớp hỗ trợ làm sạch, đối soát và liên kết dữ liệu có kiểm soát.

## 3. Dự án thực hiện điều đó như thế nào?

### 3.1. Tách biệt dữ liệu theo tenant

Mỗi tài khoản thuộc một tenant và có vai trò **Admin** hoặc **User**. Mọi dataset, bản ghi và quy trình xử lý đều được gắn với `tenant_id` để giới hạn phạm vi truy cập.

- User có thể upload và xử lý dữ liệu của tenant mình.
- Admin quản lý người dùng, tạo phiên phân tích, phê duyệt yêu cầu truy cập và thực hiện export.
- Một tenant không được tự ý xem dữ liệu thật của tenant khác.

### 3.2. Tiếp nhận dữ liệu CSV

Người dùng upload file CSV lên hệ thống. Backend kiểm tra định dạng, đọc dữ liệu theo luồng, tạo dataset và lưu các bản ghi vào MongoDB theo đúng tenant sở hữu.

Hệ thống hỗ trợ upload theo từng phần để xử lý file lớn, theo dõi tiến độ và hạn chế việc nạp toàn bộ file vào bộ nhớ cùng lúc.

### 3.3. AI đề xuất rule làm sạch

Hệ thống lấy mẫu và phân tích dữ liệu để phát hiện các lỗi hoặc sự không nhất quán. Cleaning Agent đề xuất rule kèm thông tin như:

- Trường dữ liệu cần xử lý.
- Kiểu lỗi được phát hiện.
- Phép biến đổi đề xuất.
- Ví dụ trước và sau khi làm sạch.
- Số lượng bản ghi dự kiến bị ảnh hưởng.

Người dùng có thể chọn hai chế độ:

- **Manual:** xem, duyệt, từ chối hoặc chỉnh sửa rule theo từng vòng.
- **Auto:** hệ thống tự chạy trong số vòng được cấu hình; người dùng vẫn có thể tạm dừng để kiểm tra và can thiệp.

AI chỉ đưa ra đề xuất. Rule sau khi được chấp nhận sẽ được thực thi bởi một **deterministic engine** để kết quả có thể kiểm tra, tái hiện và hoàn tác.

### 3.4. Dry-run, áp dụng và kiểm tra kết quả

Trước khi thay đổi dữ liệu thật, hệ thống chạy dry-run để hiển thị phần khác biệt giữa dữ liệu cũ và dữ liệu dự kiến sau xử lý.

Sau khi được xác nhận:

1. Rule được áp dụng lên dataset.
2. Kết quả được kiểm tra lại.
3. Bản ghi được phân loại thành dữ liệu sạch và dữ liệu còn cần review.
4. Lịch sử từng vòng và phiên bản dữ liệu được lưu lại.
5. Người dùng có thể tiếp tục vòng làm sạch mới hoặc rollback về phiên bản trước.

### 3.5. Tạo phiên matching giữa nhiều tenant

Admin tạo một session phân tích và mời các tenant khác tham gia. Mỗi tenant tự chọn dataset và các field mà mình đồng ý đóng góp.

Hệ thống chỉ sử dụng những field đã được consent. Các field nhạy cảm được cảnh báo để Admin cân nhắc trước khi chia sẻ hoặc sử dụng cho matching.

### 3.6. Mapping, blocking và chấm điểm khớp

Sau khi các bên đồng ý tham gia, hệ thống thực hiện:

1. **Schema Mapping:** AI gợi ý ánh xạ các cột có cùng ý nghĩa, ví dụ `phone_number` với `SĐT`.
2. **Weight Suggestion:** đề xuất trọng số cho từng field dựa trên độ tin cậy và độ đầy đủ của dữ liệu.
3. **Blocking:** nhóm trước các bản ghi có khả năng liên quan để tránh phải so sánh toàn bộ `n × m` cặp bản ghi.
4. **Scoring:** so sánh chính xác với các định danh mạnh và so sánh tương đồng với tên, địa chỉ hoặc các field có thể sai lệch nhẹ.
5. **Decision:** phân loại kết quả thành khớp, không khớp hoặc cần con người review.

Kết quả liên kết được lưu dưới dạng **Link Table**, gồm mã tham chiếu, điểm số và các field khớp; bảng này không chứa toàn bộ dữ liệu thật của tenant đối tác.

### 3.7. Bảo vệ dữ liệu khi xem và xuất kết quả

Kết quả xuyên tenant được che một phần (masked) theo mặc định. Nếu người dùng cần xem dữ liệu đầy đủ, họ phải gửi yêu cầu kèm lý do tới Admin của tenant sở hữu dữ liệu.

Chỉ sau khi yêu cầu được phê duyệt, dữ liệu thuộc đúng phạm vi cho phép mới được cung cấp. Quyền export chỉ dành cho Admin; dữ liệu thật của tenant khác không được xuất nếu chưa có phê duyệt tương ứng.

### 3.8. Audit log và khả năng truy vết

Các hành động quan trọng được ghi vào Audit Log, bao gồm:

- Ai thực hiện hành động.
- Hành động gì đã được thực hiện.
- Thời điểm thực hiện.
- Đối tượng hoặc tài nguyên liên quan.
- Trạng thái phê duyệt và metadata cần thiết.

Audit Log giúp kiểm tra lịch sử xử lý, điều tra sự cố và chứng minh rằng việc truy cập hoặc chia sẻ dữ liệu đã đi qua đúng quy trình.

## 4. Luồng hoạt động tổng quát

```text
Đăng nhập
  → Upload CSV
  → AI phân tích và đề xuất rule làm sạch
  → Người dùng review rule
  → Dry-run và xem thay đổi
  → Áp dụng rule bằng deterministic engine
  → Kiểm tra dữ liệu sạch/bẩn
  → Tạo session matching
  → Các tenant chọn dataset và consent field
  → AI gợi ý mapping, trọng số và blocking strategy
  → Chạy matching và chấm điểm
  → Hiển thị kết quả masked
  → Gửi yêu cầu nếu cần xem dữ liệu đầy đủ
  → Admin phê duyệt hoặc từ chối
  → Ghi Audit Log và export có kiểm soát
```

## 5. Kiến trúc triển khai

- **Frontend:** React, Vite và React Router, cung cấp giao diện upload, cleaning, matching, review và quản trị.
- **Backend:** FastAPI cung cấp REST API, xác thực, phân quyền và điều phối các workflow.
- **AI layer:** các agent hỗ trợ đề xuất cleaning rule, schema mapping và blocking strategy.
- **Processing layer:** deterministic engine thực thi các rule đã được phê duyệt và kiểm tra tính nhất quán.
- **Database:** MongoDB lưu tài khoản, tenant, dataset, workflow state, link record và audit log.
- **Deployment:** Docker Compose dùng để chạy ứng dụng và MongoDB đồng bộ trong môi trường local hoặc demo.

Tóm lại, DataUnifi kết hợp **AI hỗ trợ ra quyết định**, **con người phê duyệt**, **xử lý xác định có thể kiểm chứng** và **kiểm soát truy cập theo tenant** để làm sạch và ghép nối dữ liệu khách hàng một cách an toàn.
