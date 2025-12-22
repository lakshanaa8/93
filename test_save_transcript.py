from pymongo import MongoClient
from datetime import datetime, timezone
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

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
        print(f"Unexpected error: {e}")
        raise

# Test
if __name__ == "__main__":
    call_id = 5  # use the same call_id returned from save_call()
    transcript_text = "Patient says they have a fever"
    
    try:
        inserted_id = save_transcript(call_id, transcript_text, "en")
        print("Transcript saved in MongoDB for call_id:", call_id)
        print("MongoDB document ID:", inserted_id)
    except Exception as e:
        print(f"Failed to save transcript: {e}")

