# Bài tập XPath - Hệ thống quản lý sinh viên

## Tổng quan
File này chứa các ghi chú chi tiết về 19 truy vấn XPath được thực hiện trên file `sinhvien.xml`.

## Cấu trúc XML
```xml
<students>
    <student>
        <id>SV01</id>
        <name>Nguyễn Thị Thanh Thúy</name>
        <date>1997-12-20</date>
    </student>
    <!-- ... các sinh viên khác ... -->
    <enrollment>
        <studentRef>SV01</studentRef>
        <course>Toan101</course>
    </enrollment>
    <!-- ... các đăng ký khác ... -->
</students>
```

## Các truy vấn XPath và ghi chú

### 1. Lấy tất cả sinh viên
**XPath:** `//student`
**Ghi chú:** 
- Sử dụng `//` để tìm kiếm ở mọi cấp độ trong cây XML
- Trả về tất cả các element `<student>` trong document
- Kết quả: 5 sinh viên (SV01, SV02, SV03, SV04, SV05)

### 2. Liệt kê tên tất cả sinh viên
**XPath:** `//student/name/text()`
**Ghi chú:**
- `//student/name` tìm tất cả element `<name>` con của `<student>`
- `/text()` lấy nội dung text của element
- Kết quả: Danh sách tên 5 sinh viên

### 3. Lấy tất cả id của sinh viên
**XPath:** `//student/id/text()`
**Ghi chú:**
- Tương tự truy vấn 2, nhưng lấy element `<id>`
- Kết quả: SV01, SV02, SV03, SV04, SV05

### 4. Lấy ngày sinh của sinh viên có id = "SV01"
**XPath:** `//student[id="SV01"]/date/text()`
**Ghi chú:**
- `[id="SV01"]` là predicate để lọc sinh viên có id cụ thể
- Predicate được đặt trong dấu ngoặc vuông
- Kết quả: 1997-12-20

### 5. Lấy các khóa học
**XPath:** `//enrollment/course/text()`
**Ghi chú:**
- Tìm tất cả element `<course>` trong `<enrollment>`
- Kết quả: Toan101, Vatly203, Vatly203 (có 2 sinh viên học Vatly203)

### 6. Lấy toàn bộ thông tin của sinh viên đầu tiên
**XPath:** `//student[1]`
**Ghi chú:**
- `[1]` là predicate để lấy element đầu tiên
- Chỉ số trong XPath bắt đầu từ 1 (không phải 0)
- Kết quả: Toàn bộ element `<student>` đầu tiên

### 7. Lấy mã sinh viên đăng ký khóa học "Vatly203"
**XPath:** `//enrollment[course="Vatly203"]/studentRef/text()`
**Ghi chú:**
- Tìm `<enrollment>` có `<course>` = "Vatly203"
- Lấy `<studentRef>` của enrollment đó
- Kết quả: SV02, SV03

### 8. Lấy tên sinh viên học môn "Toan101"
**XPath:** `//student[id=//enrollment[course="Toan101"]/studentRef]/name/text()`
**Ghi chú:**
- Truy vấn lồng nhau: tìm studentRef từ enrollment có course="Toan101"
- So sánh id của student với studentRef tìm được
- Kết quả: Nguyễn Thị Thanh Thúy

### 9. Lấy tên sinh viên học môn "Vatly203"
**XPath:** `//student[id=//enrollment[course="Vatly203"]/studentRef]/name/text()`
**Ghi chú:**
- Tương tự truy vấn 8, nhưng cho môn Vatly203
- Kết quả: Lê Thị Hồng Cầm (có 2 sinh viên cùng tên)

### 10. Lấy ngày sinh của sinh viên có id="SV01"
**XPath:** `//student[id="SV01"]/date/text()`
**Ghi chú:**
- Giống hệt truy vấn 4
- Kết quả: 1997-12-20

### 11. Lấy tên và ngày sinh của mọi sinh viên sinh năm 1997
**XPath:** `//student[starts-with(date, "1997")]`
**Ghi chú:**
- `starts-with()` là function để kiểm tra chuỗi bắt đầu bằng gì
- Kiểm tra date bắt đầu bằng "1997"
- Kết quả: 2 sinh viên sinh năm 1997

### 12. Lấy tên của các sinh viên có ngày sinh trước năm 1998
**XPath:** `//student[date < "1998-01-01"]/name/text()`
**Ghi chú:**
- So sánh ngày tháng trong XPath
- `<` là toán tử so sánh nhỏ hơn
- Kết quả: Không có sinh viên nào (tất cả đều sinh từ 1997 trở đi)

### 13. Đếm tổng số sinh viên
**XPath:** `count(//student)`
**Ghi chú:**
- `count()` là function đếm số lượng element
- Kết quả: 5.0

### 14. Lấy tất cả sinh viên chưa đăng ký môn nào
**XPath:** `//student[id != //enrollment/studentRef]`
**Ghi chú:**
- `!=` là toán tử "không bằng"
- So sánh id của student với tất cả studentRef trong enrollment
- Kết quả: SV04, SV05 (2 sinh viên mới thêm chưa đăng ký môn)

### 15. Lấy phần tử `<date>` anh em ngay sau `<name>` của SV01
**XPath:** `//student[id="SV01"]/name/following-sibling::date`
**Ghi chú:**
- `following-sibling::` là axis để tìm element anh em cùng cấp
- Tìm element `<date>` ngay sau `<name>` trong cùng parent
- Kết quả: 1997-12-20

### 16. Lấy phần tử `<id>` anh em ngay trước `<name>` của SV02
**XPath:** `//student[id="SV02"]/name/preceding-sibling::id`
**Ghi chú:**
- `preceding-sibling::` là axis để tìm element anh em trước đó
- Tìm element `<id>` ngay trước `<name>` trong cùng parent
- Kết quả: SV02

### 17. Lấy toàn bộ node `<course>` trong cùng một `<enrollment>` với studentRef='SV03'
**XPath:** `//enrollment[studentRef="SV03"]/course`
**Ghi chú:**
- Tìm enrollment có studentRef="SV03"
- Lấy tất cả element `<course>` trong enrollment đó
- Kết quả: Vatly203

### 18. Lấy sinh viên có họ là "Trần"
**XPath:** `//student[contains(name, "Trần")]`
**Ghi chú:**
- `contains()` function kiểm tra chuỗi có chứa substring không
- Tìm name chứa "Trần"
- Kết quả: SV04 - Trần Văn Minh

### 19. Lấy năm sinh của sinh viên SV01
**XPath:** `substring(//student[id="SV01"]/date/text(), 1, 4)`
**Ghi chú:**
- `substring()` function cắt chuỗi
- Tham số: (chuỗi, vị trí bắt đầu, độ dài)
- Lấy 4 ký tự đầu từ vị trí 1 (năm)
- Kết quả: 1997

## Các khái niệm XPath quan trọng

### Axes (Trục)
- `//` - Descendant (con cháu ở mọi cấp)
- `following-sibling::` - Anh em sau
- `preceding-sibling::` - Anh em trước

### Functions (Hàm)
- `text()` - Lấy nội dung text
- `count()` - Đếm element
- `starts-with()` - Kiểm tra bắt đầu chuỗi
- `contains()` - Kiểm tra chứa chuỗi
- `substring()` - Cắt chuỗi

### Predicates (Điều kiện)
- `[1]` - Vị trí đầu tiên
- `[id="SV01"]` - Điều kiện bằng
- `[date < "1998-01-01"]` - Điều kiện so sánh
- `[id != //enrollment/studentRef]` - Điều kiện không bằng

### Operators (Toán tử)
- `=` - Bằng
- `!=` - Không bằng
- `<` - Nhỏ hơn
- `>` - Lớn hơn

## Chạy script
```bash
python xpath_queries.py
```

## Files trong project
- `sinhvien.xml` - File XML chứa dữ liệu sinh viên
- `xpath_queries.py` - Script Python thực hiện các truy vấn XPath
- `README.md` - File này
