#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laragon Database Setup Script
Tạo database cho ứng dụng XML Processor trên Laragon
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Fix encoding cho Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def setup_laragon_database():
    """Setup database cho Laragon"""
    
    print("Laragon Database Setup")
    print("=" * 40)
    
    # Cấu hình Laragon (mặc định không có password)
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Laragon mặc định không có password
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    try:
        print("Dang ket noi MySQL...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Tạo database
        print("Dang tao database xml_processor_db...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS xml_processor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Chọn database
        cursor.execute("USE xml_processor_db")
        
        # Tạo bảng Categories
        print("Dang tao bang Categories...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Categories (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Tạo bảng Products
        print("Dang tao bang Products...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                currency VARCHAR(10) NOT NULL,
                stock INT NOT NULL DEFAULT 0,
                category_id VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES Categories(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        connection.commit()
        
        print("Setup hoan thanh!")
        print("\nThong tin ket noi:")
        print("   Host: localhost")
        print("   Database: xml_processor_db")
        print("   User: root")
        print("   Password: (khong co)")
        print("   Port: 3306 (Laragon mac dinh)")
        
        print("\nBay gio ban co the chay:")
        print("   python xml_processor.py")
        
    except Error as e:
        print(f"Loi setup: {e}")
        print("\nKiem tra:")
        print("   1. Laragon da khoi dong MySQL chua?")
        print("   2. MySQL dang chay tren port 3306?")
        print("   3. Co the ket noi bang phpMyAdmin khong?")
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Da dong ket noi")

if __name__ == "__main__":
    setup_laragon_database()
