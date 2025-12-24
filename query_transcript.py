from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client["transcription_db"]
    collection = db["transcripts"]
    
    call_id = 5
    print(f"Finding transcripts for call_id: {call_id}\n")
    print("=" * 60)
    
    found_any = False
    for doc in collection.find({"call_id": call_id}):
        found_any = True
        print(doc)
        print("-" * 60)
    
    if not found_any:
        print(f"No transcripts found for call_id: {call_id}")
        
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print("ERROR: MongoDB server is not running or not accessible.")
    print("Please ensure MongoDB is installed and the service is running.")
    print("On Windows, you can start it with: net start MongoDB")
    print(f"Original error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")


