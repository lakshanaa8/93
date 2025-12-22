"""
PostgreSQL Connection Checker
This script helps diagnose PostgreSQL connection issues.
"""
import psycopg2
from psycopg2 import OperationalError
import subprocess
import sys

def check_postgresql_service():
    """Check if PostgreSQL service is running on Windows"""
    print("=" * 60)
    print("Checking PostgreSQL Service Status...")
    print("=" * 60)
    
    try:
        # Try to find PostgreSQL services
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Service | Where-Object {$_.DisplayName -like "*PostgreSQL*"} | Select-Object Name, Status, DisplayName | Format-Table -AutoSize'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.stdout.strip():
            print("\nFound PostgreSQL services:")
            print(result.stdout)
        else:
            print("\n[WARNING] No PostgreSQL services found.")
            print("   PostgreSQL may not be installed.")
            print("   Download from: https://www.postgresql.org/download/windows/")
            return None
            
    except Exception as e:
        print(f"\n[WARNING] Could not check services: {e}")
        return None

def check_postgresql_connection():
    """Try to connect to PostgreSQL"""
    print("\n" + "=" * 60)
    print("Testing PostgreSQL Connection...")
    print("=" * 60)
    
    config = {
        "host": "localhost",
        "database": "crm_db",
        "user": "postgres",
        "password": "abcd",
        "port": 5432
    }
    
    try:
        print(f"\nAttempting to connect to:")
        print(f"  Host: {config['host']}")
        print(f"  Port: {config['port']}")
        print(f"  Database: {config['database']}")
        print(f"  User: {config['user']}")
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print("\n[SUCCESS] PostgreSQL is running and accessible.")
        print(f"\nPostgreSQL Version: {version}")
        return True
        
    except OperationalError as e:
        error_msg = str(e)
        print("\n[FAILED] CONNECTION FAILED")
        
        if "Connection refused" in error_msg or "could not connect" in error_msg.lower():
            print("\n[DIAGNOSIS] PostgreSQL server is not running or not accepting connections.")
            print("\n[SOLUTIONS]")
            print("   1. Start PostgreSQL service:")
            print("      - Open Services (services.msc)")
            print("      - Find 'postgresql-x64-XX' service")
            print("      - Right-click -> Start")
            print("\n   2. Or use PowerShell (as Administrator):")
            print("      Get-Service | Where-Object {$_.DisplayName -like '*PostgreSQL*'}")
            print("      net start postgresql-x64-18  # Use your version number")
            print("\n   3. Check if PostgreSQL is installed:")
            print("      - Look in: C:\\Program Files\\PostgreSQL\\")
            print("      - Or check: Control Panel -> Programs")
        elif "password authentication failed" in error_msg.lower():
            print("\n[DIAGNOSIS] Password is incorrect.")
            print("   Update the password in your connection code.")
        elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
            print("\n[DIAGNOSIS] Database 'crm_db' does not exist.")
            print("   Create it with: CREATE DATABASE crm_db;")
        else:
            print(f"\n[ERROR] Error details: {error_msg}")
        
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("PostgreSQL Connection Diagnostic Tool")
    print("=" * 60)
    
    # Check service status
    check_postgresql_service()
    
    # Try connection
    success = check_postgresql_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] All checks passed! PostgreSQL is ready to use.")
    else:
        print("[FAILED] Issues detected. Please follow the suggestions above.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

