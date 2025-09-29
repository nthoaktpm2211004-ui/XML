## So sánh xs:ID và xs:unique

| Tiêu chí | xs:ID | xs:unique |
|---|---|---|
| Loại | Kiểu dữ liệu dựng sẵn (ID/IDREF) | Ràng buộc (constraint) |
| Phạm vi | Toàn bộ tài liệu XML (giá trị ID duy nhất toàn cục) | Cục bộ trong phạm vi phần tử cha (selector) |
| Tính tham chiếu | Hỗ trợ tham chiếu qua `xs:IDREF`/`xs:IDREFS` | Không có tham chiếu |
| Hạn chế cú pháp | Chỉ dùng làm thuộc tính, kiểu `xs:ID` | Áp dụng lên phần tử/thuộc tính bất kỳ theo XPATH field |
| Khi nào dùng | Cần khóa chính toàn tài liệu và liên kết bằng tham chiếu | Cần ràng buộc duy nhất trong một tập con (ví dụ danh sách con) |
| Khóa chính toàn tài liệu | ✔ | ✘ |
| Khóa duy nhất theo phạm vi tùy chỉnh | ✘ | ✔ |
| Cục bộ trong phạm vi phần tử cha | ✘ | ✔ |
| Toàn bộ tài liệu XML | ✔ | ✘ |
| Liên quan đến tính duy nhất | ✔ | ✔ |
| Kiểu dữ liệu dựng sẵn | ✔ | ✘ |
| Ràng buộc | ✘ | ✔ |


