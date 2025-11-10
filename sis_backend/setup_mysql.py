#!/usr/bin/env python
"""
Helper script to set up MySQL database for SIS
Run this before running migrations if you need to create the database
"""
import pymysql
import getpass
import sys

def setup_mysql():
    print("=" * 60)
    print("MySQL Database Setup for SIS")
    print("=" * 60)
    
    # Get MySQL root credentials
    host = input("MySQL Host (default: localhost): ").strip() or "localhost"
    root_user = input("MySQL Root Username (default: root): ").strip() or "root"
    root_password = getpass.getpass("MySQL Root Password: ")
    
    # Database details
    db_name = input("Database Name (default: sis_db): ").strip() or "sis_db"
    db_user = input("Database User (default: sis_user): ").strip() or "sis_user"
    db_password = getpass.getpass("Database User Password (default: sis_password): ") or "sis_password"
    
    try:
        # Connect to MySQL server
        print(f"\nConnecting to MySQL at {host}...")
        connection = pymysql.connect(
            host=host,
            user=root_user,
            password=root_password
        )
        cursor = connection.cursor()
        
        # Create database
        print(f"Creating database '{db_name}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Create user and grant privileges
        print(f"Creating user '{db_user}' and granting privileges...")
        cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("✓ MySQL setup completed successfully!")
        print("=" * 60)
        print(f"\nDatabase Configuration:")
        print(f"  Database Name: {db_name}")
        print(f"  User: {db_user}")
        print(f"  Password: {db_password}")
        print(f"  Host: {host}")
        print(f"\nUpdate your settings.py DATABASES configuration with these values.")
        print("\nNext steps:")
        print("  1. Update sis_backend/settings.py with the above credentials")
        print("  2. Run: python manage.py migrate")
        print("  3. Run: python manage.py createsuperuser")
        print("  4. Run: python manage.py runserver")
        
    except pymysql.Error as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease check your MySQL credentials and try again.")
        sys.exit(1)

if __name__ == "__main__":
    setup_mysql()
