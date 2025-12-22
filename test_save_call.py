import psycopg2
from psycopg2 import OperationalError, IntegrityError

def save_call(patient_id, audio_file_path, call_status='pending'):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="crm_db",
            user="postgres",
            password="abcd"  # replace with your PostgreSQL password
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calls (patient_id, audio_file_url, call_status) VALUES (%s, %s, %s) RETURNING call_id;",
            (patient_id, audio_file_path, call_status)
        )
        call_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return call_id
    except OperationalError as e:
        error_msg = str(e)
        if "Connection refused" in error_msg or "could not connect" in error_msg.lower():
            print("ERROR: PostgreSQL server is not running or not accessible.")
            print("Please ensure PostgreSQL is installed and the service is running.")
            print("On Windows, you can start it with: net start postgresql-x64-XX")
            print(f"Original error: {error_msg}")
        else:
            print(f"Database connection error: {error_msg}")
        raise
    except IntegrityError as e:
        error_msg = str(e)
        if "foreign key constraint" in error_msg.lower() and "patient_id" in error_msg.lower():
            print("ERROR: Foreign key constraint violation - Patient does not exist.")
            print(f"Patient ID {patient_id} is not present in the 'patients' table.")
            print("\nSOLUTION:")
            print("  1. Create the patient first using: python manage_patients.py create")
            print(f"  2. Or use an existing patient_id")
            print(f"  3. Check existing patients: python manage_patients.py list")
            print(f"\nOriginal error: {error_msg}")
        else:
            print(f"Database integrity error: {error_msg}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

# Test
if __name__ == "__main__":
    patient_id = 1  # make sure this patient exists in your patients table
    audio_file_path = r"C:\Users\Welcome\PHOENIXIX\audio_files\call_123.wav"
    try:
        call_id = save_call(patient_id, audio_file_path)
        print("Inserted call_id in CRM:", call_id)
    except Exception as e:
        print(f"Failed to save call: {e}")