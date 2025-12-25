"""
Patient Management Script
Helps create and list patients in the CRM database.
"""
import psycopg2
from psycopg2 import OperationalError, IntegrityError
import sys

def get_connection():
    """Get database connection"""
    return psycopg2.connect(
        host="localhost",
        database="crm_db",
        user="postgres",
        password="abcd"
    )

def create_patient(phone_number=None):
    """Create a new patient"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if phone_number:
            cursor.execute(
                "INSERT INTO patients (phone_number) VALUES (%s) RETURNING patient_id;",
                (phone_number,)
            )
        else:
            cursor.execute(
                "INSERT INTO patients DEFAULT VALUES RETURNING patient_id;"
            )
        
        patient_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"[SUCCESS] Created patient with ID: {patient_id}")
        if phone_number:
            print(f"  Phone number: {phone_number}")
        return patient_id
        
    except OperationalError as e:
        print(f"[ERROR] Database connection failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to create patient: {e}")
        return None

def list_patients():
    """List all patients"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id, phone_number, created_at FROM patients ORDER BY patient_id;")
        patients = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not patients:
            print("[INFO] No patients found in the database.")
            print("Create one with: python manage_patients.py create")
            return
        
        print("\n" + "=" * 60)
        print("Patients in Database")
        print("=" * 60)
        print(f"{'ID':<10} {'Phone Number':<20} {'Created At'}")
        print("-" * 60)
        for patient_id, phone_number, created_at in patients:
            phone = phone_number if phone_number else "(none)"
            print(f"{patient_id:<10} {phone:<20} {created_at}")
        print("=" * 60 + "\n")
        
    except OperationalError as e:
        print(f"[ERROR] Database connection failed: {e}")
    except Exception as e:
        print(f"[ERROR] Failed to list patients: {e}")

def check_patient_exists(patient_id):
    """Check if a patient exists"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id FROM patients WHERE patient_id = %s;", (patient_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"[ERROR] Failed to check patient: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_patients.py create [phone_number]  - Create a new patient")
        print("  python manage_patients.py list                   - List all patients")
        print("  python manage_patients.py check <patient_id>     - Check if patient exists")
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        phone_number = sys.argv[2] if len(sys.argv) > 2 else None
        create_patient(phone_number)
    elif command == "list":
        list_patients()
    elif command == "check":
        if len(sys.argv) < 3:
            print("[ERROR] Please provide a patient_id")
            print("Usage: python manage_patients.py check <patient_id>")
            return
        patient_id = int(sys.argv[2])
        exists = check_patient_exists(patient_id)
        if exists:
            print(f"[SUCCESS] Patient ID {patient_id} exists.")
        else:
            print(f"[INFO] Patient ID {patient_id} does NOT exist.")
            print("Create it with: python manage_patients.py create")
    else:
        print(f"[ERROR] Unknown command: {command}")
        print("Use 'create', 'list', or 'check'")

if __name__ == "__main__":
    main()



