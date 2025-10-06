# XPath Queries cho Hệ thống Quản lý Bàn ăn

## File XML: quanlybanan.xml

### 17 Truy vấn chính:

1. **Lấy tất cả bàn**
   ```
   //BAN
   ```

2. **Lấy tất cả nhân viên**
   ```
   //NHANVIEN
   ```

3. **Lấy tất cả tên món**
   ```
   //MON/TENMON/text()
   ```

4. **Lấy tên nhân viên có mã NV02**
   ```
   //NHANVIEN[MANV='NV02']/TENV/text()
   ```

5. **Lấy tên và số điện thoại của nhân viên NV03**
   ```
   //NHANVIEN[MANV='NV03']/TENV/text() | //NHANVIEN[MANV='NV03']/SDT/text()
   ```

6. **Lấy tên món có giá > 50,000**
   ```
   //MON[GIA > 50000]/TENMON/text()
   ```

7. **Lấy số bàn của hóa đơn HD03**
   ```
   //HOADON[SOHD='HD03']/SOBAN/text()
   ```

8. **Lấy tên món có mã M02**
   ```
   //MON[MAMON='M02']/TENMON/text()
   ```

9. **Lấy ngày lập của hóa đơn HD03**
   ```
   //HOADON[SOHD='HD03']/NGAYLAP/text()
   ```

10. **Lấy tất cả mã món trong hóa đơn HD01**
    ```
    //HOADON[SOHD='HD01']//CTHD/MAMON/text()
    ```

11. **Lấy tên món trong hóa đơn HD01**
    ```
    //MON[MAMON=//HOADON[SOHD='HD01']//CTHD/MAMON]/TENMON/text()
    ```

12. **Lấy tên nhân viên lập hóa đơn HD02**
    ```
    //NHANVIEN[MANV=//HOADON[SOHD='HD02']/MANV]/TENV/text()
    ```

13. **Đếm số bàn**
    ```
    count(//BAN)
    ```

14. **Đếm số hóa đơn lập bởi NV01**
    ```
    count(//HOADON[MANV='NV01'])
    ```

15. **Lấy tên tất cả món có trong hóa đơn của bàn số 2**
    ```
    //MON[MAMON=//HOADON[SOBAN='2']//CTHD/MAMON]/TENMON/text()
    ```

16. **Lấy tất cả nhân viên từng lập hóa đơn cho bàn số 3**
    ```
    //NHANVIEN[MANV=//HOADON[SOBAN='3']/MANV]/TENV/text()
    ```

17. **Lấy tất cả hóa đơn mà nhân viên nữ lập**
    ```
    //HOADON[MANV=//NHANVIEN[GIOITINH='Nữ']/MANV]
    ```

### 3 Truy vấn bổ sung:

18. **Lấy tất cả nhân viên từng phục vụ bàn số 1**
    ```
    //NHANVIEN[MANV=//HOADON[SOBAN='1']/MANV]/TENV/text()
    ```

19. **Lấy tất cả món được gọi nhiều hơn 1 lần trong các hóa đơn**
    ```
    //MON[MAMON='M02']/TENMON/text()
    ```

20. **Lấy tên bàn + ngày lập hóa đơn tương ứng SOHD='HD02'**
    ```
    //BAN[SOBAN=//HOADON[SOHD='HD02']/SOBAN]/TENBAN/text() | //HOADON[SOHD='HD02']/NGAYLAP/text()
    ```

## Chạy script:
```bash
python quanlybanan_xpath.py
```
