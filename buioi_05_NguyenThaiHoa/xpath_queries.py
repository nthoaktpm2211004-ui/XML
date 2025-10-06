from lxml import etree
import re
import sys
import io

# Thiết lập mã hóa UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Đọc file XML
def load_xml(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return etree.parse(file)

# Thực hiện truy vấn XPath và hiển thị kết quả
def execute_xpath_query(tree, xpath, description):
    print(f"\n{description}")
    print(f"XPath: {xpath}")
    try:
        result = tree.xpath(xpath)
        if isinstance(result, list):
            if len(result) == 0:
                print("Kết quả: Không có kết quả phù hợp")
            else:
                print(f"Kết quả ({len(result)} mục):")
                for i, item in enumerate(result, 1):
                    if hasattr(item, 'text'):
                        print(f"  {i}. {item.text}")
                    else:
                        print(f"  {i}. {item}")
        else:
            print(f"Kết quả: {result}")
    except Exception as e:
        print(f"Lỗi: {e}")
    print("-" * 50)

def main():
    print("=== Bài tập XPath - Hệ thống quản lý sinh viên ===")
    
    # Tải file XML
    tree = load_xml('sinhvien.xml')
    
    # 1. Lấy tất cả sinh viên
    execute_xpath_query(tree, '//student', "1. Lấy tất cả sinh viên")
    
    # 2. Liệt kê tên tất cả sinh viên
    execute_xpath_query(tree, '//student/name/text()', "2. Liệt kê tên tất cả sinh viên")
    
    # 3. Lấy tất cả id của sinh viên
    execute_xpath_query(tree, '//student/id/text()', "3. Lấy tất cả id của sinh viên")
    
    # 4. Lấy ngày sinh của sinh viên có id = "SV01"
    execute_xpath_query(tree, '//student[id="SV01"]/date/text()', "4. Lấy ngày sinh của sinh viên có id = 'SV01'")
    
    # 5. Lấy các khóa học
    execute_xpath_query(tree, '//enrollment/course/text()', "5. Lấy các khóa học")
    
    # 6. Lấy toàn bộ thông tin của sinh viên đầu tiên
    execute_xpath_query(tree, '//student[1]', "6. Lấy toàn bộ thông tin của sinh viên đầu tiên")
    
    # 7. Lấy mã sinh viên đăng ký khóa học "Vatly203"
    execute_xpath_query(tree, '//enrollment[course="Vatly203"]/studentRef/text()', "7. Lấy mã sinh viên đăng ký khóa học 'Vatly203'")
    
    # 8. Lấy tên sinh viên học môn "Toan101"
    execute_xpath_query(tree, '//student[id=//enrollment[course="Toan101"]/studentRef]/name/text()', "8. Lấy tên sinh viên học môn 'Toan101'")
    
    # 9. Lấy tên sinh viên học môn "Vatly203"
    execute_xpath_query(tree, '//student[id=//enrollment[course="Vatly203"]/studentRef]/name/text()', "9. Lấy tên sinh viên học môn 'Vatly203'")
    
    # 10. Lấy ngày sinh của sinh viên có id="SV01"
    execute_xpath_query(tree, '//student[id="SV01"]/date/text()', "10. Lấy ngày sinh của sinh viên có id='SV01'")
    
    # 11. Lấy tên và ngày sinh của mọi sinh viên sinh năm 1997
    execute_xpath_query(tree, '//student[starts-with(date, "1997")]', "11. Lấy tên và ngày sinh của mọi sinh viên sinh năm 1997")
    
    # 12. Lấy tên của các sinh viên có ngày sinh trước năm 1998
    execute_xpath_query(tree, '//student[date < "1998-01-01"]/name/text()', "12. Lấy tên của các sinh viên có ngày sinh trước năm 1998")
    
    # 13. Đếm tổng số sinh viên
    execute_xpath_query(tree, 'count(//student)', "13. Đếm tổng số sinh viên")
    
    # 14. Lấy tất cả sinh viên chưa đăng ký môn nào
    execute_xpath_query(tree, '//student[id != //enrollment/studentRef]', "14. Lấy tất cả sinh viên chưa đăng ký môn nào")
    
    # 15. Lấy phần tử <date> anh em ngay sau <name> của SV01
    execute_xpath_query(tree, '//student[id="SV01"]/name/following-sibling::date', "15. Lấy phần tử <date> anh em ngay sau <name> của SV01")
    
    # 16. Lấy phần tử <id> anh em ngay trước <name> của SV02
    execute_xpath_query(tree, '//student[id="SV02"]/name/preceding-sibling::id', "16. Lấy phần tử <id> anh em ngay trước <name> của SV02")
    
    # 17. Lấy toàn bộ node <course> trong cùng một <enrollment> với studentRef='SV03'
    execute_xpath_query(tree, '//enrollment[studentRef="SV03"]/course', "17. Lấy toàn bộ node <course> trong cùng một <enrollment> với studentRef='SV03'")
    
    # 18. Lấy sinh viên có họ là "Trần"
    execute_xpath_query(tree, '//student[contains(name, "Trần")]', "18. Lấy sinh viên có họ là 'Trần'")
    
    # 19. Lấy năm sinh của sinh viên SV01
    execute_xpath_query(tree, 'substring(//student[id="SV01"]/date/text(), 1, 4)', "19. Lấy năm sinh của sinh viên SV01")

if __name__ == "__main__":
    main()