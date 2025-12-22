import psycopg2
from pymongo import MongoClient
from datetime import datetime, timezone
from psycopg2 import OperationalError, IntegrityError
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# ----------- PostgreSQL (CRM) functions -----------

def save_call(patient_id, audio_file_path, call_status='pending'):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="crm_db",
            user="postgres",
            password="abcd"  # <-- replace with your password
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
        print(f"Unexpected error in save_call: {e}")
        raise

def update_call_status(call_id, status):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="crm_db",
            user="postgres",
            password="abcd"  # <-- replace with your password
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE calls SET call_status=%s WHERE call_id=%s;", (status, call_id))
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        
        if rows_affected == 0:
            print(f"WARNING: No call found with call_id={call_id}. Status not updated.")
        return rows_affected > 0
    except OperationalError as e:
        error_msg = str(e)
        if "Connection refused" in error_msg or "could not connect" in error_msg.lower():
            print("ERROR: PostgreSQL server is not running or not accessible.")
            print("Please ensure PostgreSQL is installed and the service is running.")
            print(f"Original error: {error_msg}")
        else:
            print(f"Database connection error: {error_msg}")
        raise
    except Exception as e:
        print(f"Unexpected error in update_call_status: {e}")
        raise

# ----------- MongoDB (Transcription) function -----------

def save_transcript(call_id, transcript_text, language="en"):
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["transcription_db"]
        collection = db["transcripts"]
        result = collection.insert_one({
            "call_id": call_id,
            "transcript_text": transcript_text,
            "language": language,
            "created_at": datetime.now(timezone.utc)
        })
        return result.inserted_id
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print("ERROR: MongoDB server is not running or not accessible.")
        print("Please ensure MongoDB is installed and the service is running.")
        print("On Windows, you can start it with: net start MongoDB")
        print(f"Original error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error in save_transcript: {e}")
        raise

# ----------- Demo workflow -----------

if __name__ == "__main__":
    try:
        # 1. Insert a dummy patient (or use existing patient_id)
        patient_id = 1  # replace with a valid patient_id from your patients table
        
        # 2. Save audio call in CRM
        audio_file_path = "C:\\Users\\Welcome\\PHOENIXIX\\audio_files\\call_123.wav"  # dummy path
        call_id = save_call(patient_id, audio_file_path)
        print(f"Inserted call_id in CRM: {call_id}")

        # 3. Save transcription in MongoDB
        transcript_text = "Patient says they have a fever"
        inserted_id = save_transcript(call_id, transcript_text, "en")
        print(f"Transcript saved in MongoDB for call_id: {call_id} (MongoDB ID: {inserted_id})")

        # 4. Update CRM call status
        update_call_status(call_id, "completed")
        print(f"CRM call_status updated for call_id: {call_id}")

        print("\nDemo workflow completed successfully!")
        
    except Exception as e:
        print(f"\nDemo workflow failed: {e}")
        print("Please check the error messages above for details.")

