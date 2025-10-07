#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML Processor - Ứng dụng xử lý XML và lưu vào MySQL
Tác giả: Nguyễn Trần Tuấn Khôi
Mô tả: Parse XML, validate với XSD, và lưu dữ liệu vào MySQL
"""

import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import Error
from lxml import etree
import sys
import os
from typing import List, Dict, Tuple, Optional

# Fix encoding cho Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class XMLProcessor:
    def __init__(self, xml_file: str, xsd_file: str, db_config: Dict):
        """
        Khởi tạo XML Processor
        
        Args:
            xml_file: Đường dẫn đến file XML
            xsd_file: Đường dẫn đến file XSD
            db_config: Cấu hình kết nối MySQL
        """
        self.xml_file = xml_file
        self.xsd_file = xsd_file
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        
    def parse_xml_xsd(self) -> Tuple[etree._Element, etree.XMLSchema]:
        """
        Parse file XML và XSD
        
        Returns:
            Tuple chứa XML root element và XMLSchema object
        """
        try:
            # Parse XML file
            print(f"📄 Đang parse file XML: {self.xml_file}")
            xml_doc = etree.parse(self.xml_file)
            xml_root = xml_doc.getroot()
            
            # Parse XSD file và tạo XMLSchema object
            print(f"📋 Đang parse file XSD: {self.xsd_file}")
            xsd_doc = etree.parse(self.xsd_file)
            xml_schema = etree.XMLSchema(xsd_doc)
            
            print("✅ Parse XML và XSD thành công!")
            return xml_root, xml_schema
            
        except etree.XMLSyntaxError as e:
            print(f"❌ Lỗi cú pháp XML: {e}")
            sys.exit(1)
        except etree.XMLSchemaParseError as e:
            print(f"❌ Lỗi parse XSD: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"❌ Không tìm thấy file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Lỗi không xác định khi parse: {e}")
            sys.exit(1)
    
    def validate_xml(self, xml_root: etree._Element, xml_schema: etree.XMLSchema) -> bool:
        """
        Validate XML với XSD
        
        Args:
            xml_root: XML root element
            xml_schema: XMLSchema object
            
        Returns:
            True nếu XML hợp lệ, False nếu không
        """
        try:
            print("🔍 Đang validate XML với XSD...")
            
            # Validate XML với XSD
            is_valid = xml_schema.validate(xml_root)
            
            if is_valid:
                print("✅ XML hợp lệ với XSD!")
                return True
            else:
                print("❌ XML không hợp lệ với XSD!")
                print("📋 Chi tiết lỗi:")
                
                # In ra các lỗi cụ thể
                for error in xml_schema.error_log:
                    print(f"   - Dòng {error.line}: {error.message}")
                
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi validate: {e}")
            return False
    
    def connect_mysql(self) -> bool:
        """
        Kết nối đến MySQL database
        
        Returns:
            True nếu kết nối thành công, False nếu không
        """
        try:
            print("🔌 Đang kết nối MySQL...")
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("✅ Kết nối MySQL thành công!")
            return True
            
        except Error as e:
            print(f"❌ Lỗi kết nối MySQL: {e}")
            return False
    
    def create_tables(self):
        """
        Tạo bảng Categories và Products nếu chưa có
        """
        try:
            print("🏗️  Đang tạo bảng...")
            
            # Tạo bảng Categories
            create_categories_table = """
            CREATE TABLE IF NOT EXISTS Categories (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            # Tạo bảng Products
            create_products_table = """
            CREATE TABLE IF NOT EXISTS Products (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                currency VARCHAR(10) NOT NULL,
                stock INT NOT NULL,
                category_id VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES Categories(id)
            )
            """
            
            self.cursor.execute(create_categories_table)
            self.cursor.execute(create_products_table)
            self.connection.commit()
            
            print("✅ Tạo bảng thành công!")
            
        except Error as e:
            print(f"❌ Lỗi tạo bảng: {e}")
            sys.exit(1)
    
    def extract_data_with_xpath(self, xml_root: etree._Element) -> Tuple[List[Dict], List[Dict]]:
        """
        Sử dụng XPath để lấy dữ liệu từ categories và products
        
        Args:
            xml_root: XML root element
            
        Returns:
            Tuple chứa danh sách categories và products
        """
        try:
            print("🔍 Đang extract dữ liệu bằng XPath...")
            
            # Extract categories bằng XPath
            categories = []
            category_elements = xml_root.xpath('//category')
            
            for category in category_elements:
                category_data = {
                    'id': category.get('id'),
                    'name': category.text.strip()
                }
                categories.append(category_data)
            
            # Extract products bằng XPath
            products = []
            product_elements = xml_root.xpath('//product')
            
            for product in product_elements:
                product_data = {
                    'id': product.get('id'),
                    'categoryRef': product.get('categoryRef'),
                    'name': product.xpath('name')[0].text.strip(),
                    'price': float(product.xpath('price')[0].text.strip()),
                    'currency': product.xpath('price')[0].get('currency'),
                    'stock': int(product.xpath('stock')[0].text.strip())
                }
                products.append(product_data)
            
            print(f"✅ Extract thành công: {len(categories)} categories, {len(products)} products")
            return categories, products
            
        except Exception as e:
            print(f"❌ Lỗi extract dữ liệu: {e}")
            sys.exit(1)
    
    def insert_or_update_categories(self, categories: List[Dict]):
        """
        Insert hoặc update dữ liệu vào bảng Categories
        
        Args:
            categories: Danh sách categories
        """
        try:
            print("📝 Đang xử lý bảng Categories...")
            
            for category in categories:
                # Kiểm tra xem category đã tồn tại chưa
                check_query = "SELECT id FROM Categories WHERE id = %s"
                self.cursor.execute(check_query, (category['id'],))
                exists = self.cursor.fetchone()
                
                if exists:
                    # Update nếu đã tồn tại
                    update_query = """
                    UPDATE Categories 
                    SET name = %s, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = %s
                    """
                    self.cursor.execute(update_query, (category['name'], category['id']))
                    print(f"   🔄 Updated category: {category['id']} - {category['name']}")
                else:
                    # Insert nếu chưa tồn tại
                    insert_query = """
                    INSERT INTO Categories (id, name) 
                    VALUES (%s, %s)
                    """
                    self.cursor.execute(insert_query, (category['id'], category['name']))
                    print(f"   ➕ Inserted category: {category['id']} - {category['name']}")
            
            self.connection.commit()
            print("✅ Xử lý bảng Categories hoàn thành!")
            
        except Error as e:
            print(f"❌ Lỗi xử lý Categories: {e}")
            self.connection.rollback()
            sys.exit(1)
    
    def insert_or_update_products(self, products: List[Dict]):
        """
        Insert hoặc update dữ liệu vào bảng Products
        
        Args:
            products: Danh sách products
        """
        try:
            print("📝 Đang xử lý bảng Products...")
            
            for product in products:
                # Kiểm tra xem product đã tồn tại chưa
                check_query = "SELECT id FROM Products WHERE id = %s"
                self.cursor.execute(check_query, (product['id'],))
                exists = self.cursor.fetchone()
                
                if exists:
                    # Update nếu đã tồn tại
                    update_query = """
                    UPDATE Products 
                    SET name = %s, price = %s, currency = %s, stock = %s, 
                        category_id = %s, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = %s
                    """
                    self.cursor.execute(update_query, (
                        product['name'], product['price'], product['currency'],
                        product['stock'], product['categoryRef'], product['id']
                    ))
                    print(f"   🔄 Updated product: {product['id']} - {product['name']}")
                else:
                    # Insert nếu chưa tồn tại
                    insert_query = """
                    INSERT INTO Products (id, name, price, currency, stock, category_id) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    self.cursor.execute(insert_query, (
                        product['id'], product['name'], product['price'],
                        product['currency'], product['stock'], product['categoryRef']
                    ))
                    print(f"   ➕ Inserted product: {product['id']} - {product['name']}")
            
            self.connection.commit()
            print("✅ Xử lý bảng Products hoàn thành!")
            
        except Error as e:
            print(f"❌ Lỗi xử lý Products: {e}")
            self.connection.rollback()
            sys.exit(1)
    
    def close_connection(self):
        """Đóng kết nối MySQL"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Đã đóng kết nối MySQL")
    
    def process(self):
        """
        Thực hiện toàn bộ quy trình xử lý
        """
        try:
            print("🚀 Bắt đầu xử lý XML...")
            print("=" * 50)
            
            # Bước 1: Parse XML và XSD
            xml_root, xml_schema = self.parse_xml_xsd()
            
            # Bước 2: Validate XML với XSD
            if not self.validate_xml(xml_root, xml_schema):
                print("❌ Dừng xử lý do XML không hợp lệ!")
                return
            
            # Bước 3: Kết nối MySQL
            if not self.connect_mysql():
                print("❌ Dừng xử lý do không thể kết nối MySQL!")
                return
            
            # Bước 4: Tạo bảng
            self.create_tables()
            
            # Bước 5: Extract dữ liệu bằng XPath
            categories, products = self.extract_data_with_xpath(xml_root)
            
            # Bước 6: Insert/Update vào MySQL
            self.insert_or_update_categories(categories)
            self.insert_or_update_products(products)
            
            print("=" * 50)
            print("🎉 Xử lý hoàn thành thành công!")
            
        except Exception as e:
            print(f"❌ Lỗi trong quá trình xử lý: {e}")
        finally:
            self.close_connection()


def main():
    """Hàm main"""
    # Cấu hình kết nối MySQL cho Laragon
    db_config = {
        'host': 'localhost',
        'database': 'xml_processor_db',
        'user': 'root',
        'password': '',  # Laragon mặc định không có password
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    # Tạo processor và thực hiện xử lý
    processor = XMLProcessor('catalog.xml', 'catalog.xsd', db_config)
    processor.process()


if __name__ == "__main__":
    main()
