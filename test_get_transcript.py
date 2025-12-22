from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import json
from datetime import datetime

def get_transcripts_by_call_id(call_id):
    """Retrieve all transcripts for a given call_id"""
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["transcription_db"]
        collection = db["transcripts"]
        
        transcripts = []
        for doc in collection.find({"call_id": call_id}):
            # Convert ObjectId to string for JSON serialization
            doc["_id"] = str(doc["_id"])
            # Convert datetime to string for better readability
            if "created_at" in doc and isinstance(doc["created_at"], datetime):
                doc["created_at"] = doc["created_at"].isoformat()
            transcripts.append(doc)
        
        return transcripts
        
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
    call_id = 5
    
    try:
        print(f"Searching for transcripts with call_id: {call_id}")
        print("=" * 60)
        
        transcripts = get_transcripts_by_call_id(call_id)
        
        if not transcripts:
            print(f"No transcripts found for call_id: {call_id}")
        else:
            print(f"Found {len(transcripts)} transcript(s):\n")
            for i, doc in enumerate(transcripts, 1):
                print(f"Transcript {i}:")
                print(json.dumps(doc, indent=2))
                print("-" * 60)
        
    except Exception as e:
        print(f"Failed to retrieve transcripts: {e}")

