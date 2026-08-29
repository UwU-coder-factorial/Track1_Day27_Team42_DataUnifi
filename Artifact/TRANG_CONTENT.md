# Phần của Trần Thị Kiều Trang - Day 27 AI Team Lab

## Trạng thái và phạm vi

- Dự án: **DataUnify** (tên sản phẩm đã được thành viên xác nhận; tên repository hiện dùng `DataUnifi`).
- Owner: Trần Thị Kiều Trang.
- Phạm vi: Trang 1 - Stakeholder Map & Strategy; phần Pitch và xử lý phản biện của Trang 2.
- Trạng thái: **CONTENT COMPLETE - SẴN SÀNG TÍCH HỢP VÀO PDF**.
- Nguyên tắc: chỉ sử dụng bằng chứng do thành viên cung cấp; không tuyên bố production-ready, có người dùng thật hoặc có đối tác pilot khi chưa được xác nhận.

## Mục tiêu 1-3 tháng đề xuất

Đưa DataUnify từ MVP/POC kỹ thuật đến trạng thái **pilot-ready**: hoàn thiện các kiểm soát bảo mật và export ưu tiên P1, xác nhận lại chất lượng Cleaning/Mapping/Matching trên dữ liệu ẩn danh hoặc gần thực tế, đồng thời chuẩn bị một pilot giới hạn có tiêu chí chấp nhận, human approval và audit rõ ràng.

---

# Trang 1 - Stakeholder Map & Strategy

## Stakeholder Map

> Quadrant được xác định bằng Influence x Interest. Nhãn Champion/Blocker/Supporter/Bystander không thay thế stance thực tế.

| # | Stakeholder cụ thể | Influence | Interest | Quadrant | Stance hiện tại | Mối quan tâm và khả năng tác động |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Nguyễn Quang Huy - owner Scope, RACI và Integration của Team 42 | Cao | Cao | Champion | Ủng hộ | Điều phối mục tiêu, RACI, tích hợp nội dung và chất lượng bản nộp. |
| 2 | Trần Thị Kiều Trang - owner Stakeholder và Pitch của Team 42 | Cao | Cao | Champion | Ủng hộ | Chịu trách nhiệm thông điệp với stakeholder, bằng chứng trong Pitch và Gate 1. |
| 3 | Nguyễn Quý Dũng - owner AI Team Design và Team Health của Team 42 | Cao | Cao | Champion | Ủng hộ | Gắn rủi ro kỹ thuật, capability gap và Growth Plan với cam kết trong Pitch. |
| 4 | Giảng viên/mentor trực tiếp chấm Lab và review dự án Team 42 | Cao | Cao | Champion | Trung lập - chờ bằng chứng | Phản biện phạm vi, độ tin cậy của bằng chứng và khả năng sẵn sàng cho pilot. |
| 5 | Head of Data/Operations có quyền duyệt pilot tại doanh nghiệp mục tiêu | Cao | Thấp hiện tại | Blocker | Chưa tiếp cận | Có thể cho phép hoặc dừng pilot; quan tâm giá trị, chi phí, bảo mật, rollback và matching sai. |
| 6 | Data Admin/Data Steward trực tiếp vận hành CSV tại doanh nghiệp mục tiêu | Thấp | Cao | Supporter | Chưa tiếp cận | Có thể cung cấp feedback workflow, dữ liệu thử an toàn và tiêu chí chấp nhận thực tế. |
| 7 | DPO/IT Security/Legal reviewer của doanh nghiệp mục tiêu | Cao | Thấp hiện tại | Blocker | Chưa tiếp cận | Có thể dừng pilot nếu masking, consent, PHI, phân quyền, audit và export control chưa đủ rõ. |

## Ma trận Influence x Interest

|  | Interest thấp | Interest cao |
| --- | --- | --- |
| **Influence cao** | **Blocker:** Head of Data/Operations; DPO/IT Security/Legal reviewer | **Champion:** Huy; Trang; Dũng; giảng viên/mentor |
| **Influence thấp** | **Bystander:** chưa xác định stakeholder phù hợp; chỉ theo dõi nếu xuất hiện | **Supporter:** Data Admin/Data Steward |

## Hai stakeholder cần tận dụng sự ủng hộ

### 1. Nguyễn Quang Huy

- Quan tâm: mục tiêu 1-3 tháng rõ ràng, RACI có một Accountable cho mỗi task và bộ PDF nhất quán.
- Có thể giúp: chốt Scope, ghép RACI vào Trang 2 và bảo đảm Pitch phù hợp kế hoạch triển khai.
- Hành động: trước **04/09/2026**, gửi Huy Stakeholder Map và Pitch; đề nghị xác nhận mục tiêu pilot-ready, stakeholder trong RACI và small ask.
- Dấu hiệu hoàn thành: Huy chấp thuận hoặc sửa trực tiếp ba nội dung trên.

### 2. Nguyễn Quý Dũng

- Quan tâm: AI Team Architecture, capability gap, chất lượng AI và Team Health.
- Có thể giúp: chuyển rủi ro trong Pitch thành capability gap và Growth Plan có owner/deadline.
- Hành động: trước **05/09/2026**, gửi Dũng phần phản biện; đề nghị gắn ít nhất một capability gap và một action 30 ngày với rủi ro eval, security hoặc production readiness.
- Dấu hiệu hoàn thành: Trang 3-4 có ít nhất một liên kết rõ với rủi ro và biện pháp giảm rủi ro trong Pitch.

## Hai stakeholder cần ưu tiên thuyết phục

### 3. Head of Data/Operations có quyền phê duyệt pilot

- Quan tâm: giá trị kinh doanh, thời gian tiết kiệm, bảo mật, chi phí và rủi ro ảnh hưởng dữ liệu production.
- Có thể cản trở: không cho truy cập dữ liệu hoặc không duyệt pilot vì chưa có người dùng thật và validation production.
- Hành động: trước **08/09/2026**, lập danh sách ít nhất ba Head of Data/Operations phù hợp, chọn một đầu mối ưu tiên và gửi lời mời demo 30 phút kèm đề xuất pilot giới hạn bằng dữ liệu synthetic/ẩn danh.
- Dấu hiệu hoàn thành: một stakeholder cụ thể nhận lời mời và phản hồi về demo hoặc điều kiện pilot.

### 4. DPO/IT Security/Legal reviewer

- Quan tâm: tenant isolation, consent, masking, PHI, quyền xem dữ liệu, audit log, export và xử lý sự cố.
- Có thể cản trở: yêu cầu dừng pilot nếu luồng dữ liệu và kiểm soát truy cập chưa được giải thích hoặc kiểm thử đầy đủ.
- Hành động: trước **11/09/2026**, tạo data-flow và checklist kiểm soát một trang; xin review về masking, approval, audit, rollback và export hardening.
- Dấu hiệu hoàn thành: nhận danh sách yêu cầu sửa hoặc xác nhận đủ điều kiện cho pilot giới hạn.

## Gate 1 - Tự kiểm tra

- [x] Có ít nhất 6 stakeholder cụ thể theo vai trò và quan hệ với DataUnify.
- [x] Mỗi stakeholder được map theo Influence x Interest.
- [x] Quadrant và stance được tách riêng.
- [x] Có 2 stakeholder cần tận dụng sự ủng hộ.
- [x] Có 2 stakeholder cần ưu tiên thuyết phục.
- [x] Bốn chiến lược có deadline và dấu hiệu hoàn thành.
- [x] Stakeholder bên ngoài được xác định ở mức vai trò ra quyết định cụ thể, không dùng nhãn chung như "khách hàng" hoặc "người dùng".
- [x] Nội dung thuộc phạm vi của Trang đã hoàn tất và sẵn sàng tích hợp.
- [ ] Huy và Dũng review bản tích hợp cuối - đây là gate cấp team, không phải nội dung còn thiếu của Trang.

---

# Trang 2 - Conclusion-First Pitch và xử lý phản biện

## Stakeholder nhận Pitch

Head of Data/Operations có quyền phê duyệt pilot tại doanh nghiệp đang có dữ liệu khách hàng phân tán trong nhiều file CSV hoặc hệ thống.

## Pitch

**Kết luận/đề xuất:** Đánh giá DataUnify bằng pilot giới hạn với dữ liệu synthetic/ẩn danh, chưa kết nối production.

**Lý do 1 - Đúng vấn đề:** DataUnify làm sạch, chuẩn hóa và ghép hồ sơ trùng lặp hoặc khác schema. Người vận hành review rule AI và dry-run trước khi áp dụng.

**Lý do 2 - Có kiểm soát:** Hệ thống multi-tenant hỗ trợ masking, consent, phân quyền, approval, rollback và audit. AI chỉ đề xuất; rule và kết quả không chắc chắn vẫn qua human review.

**Lý do 3 - Có bằng chứng MVP/POC:** Báo cáo gần nhất ghi 480 test passed; pipeline đạt 5/5 stage trên 3.600 hồ sơ synthetic; mapping offline đạt 91,67% accuracy và 90,65% Macro F1 trên 48 cases.

**Giới hạn:** Kết quả chủ yếu là synthetic/offline; chưa có feedback người dùng thật, chưa chạy lại toàn bộ 597 test và chưa production-validated.

**Small ask:** Tham gia demo 30 phút và chỉ định một data owner để chốt dữ liệu an toàn, tiêu chí chấp nhận và stop condition.

## Phản biện chính

> "Kết quả synthetic/offline chưa chứng minh DataUnify an toàn và chính xác với dữ liệu doanh nghiệp thật."

## Cách xử lý dựa trên bằng chứng và giảm rủi ro

Team không đề nghị triển khai production. Pilot chỉ dùng dữ liệu synthetic/ẩn danh, không tích hợp CRM/ERP và không tự động chấp nhận kết quả. Rule AI phải qua human approval; matching mặc định masked; trường hợp không chắc chắn được review. Team sẽ chốt trước tiêu chí chấp nhận, audit, quyền truy cập, rollback và stop condition; chỉ mở rộng khi đạt tiêu chí và qua review bảo mật.

## Điểm Huy cần ghép vào RACI

- Task "Xác định use case và tiêu chí pilot" cần Consulted/Informed đúng stakeholder nhận Pitch.
- Task "Kiểm thử quality/security" cần data owner và reviewer bảo mật ở vai trò Consulted.
- Task "Quyết định pilot/release" phải có đúng một Accountable trong Team 42.

## Nguồn bằng chứng nội bộ do thành viên cung cấp

- Live AI report: `eval/results/t031/17_agents_deep_live_retest.md` trong repo dự án.
- Manual UI evidence: `eval/results/g2_manual_evidence.md` trong repo dự án.
- Video demo: `presentation/MVP-404_Brain_Not_Found.mp4` trong repo dự án.
- Huy/Team 42 cần đối chiếu số liệu với báo cáo gốc trước khi export PDF cuối.
