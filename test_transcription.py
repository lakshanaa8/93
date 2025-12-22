from pymongo import MongoClient
from datetime import datetime

def test_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["transcription_db"]
    
    # Create a test collection and insert a dummy transcript
    collection = db["test_transcripts"]
    test_doc = {
        "call_id": 1,
        "transcript_text": "This is a test transcript",
        "language": "en",
        "created_at": datetime.utcnow()
    }
    collection.insert_one(test_doc)
    
    # Fetch documents to verify
    docs = list(collection.find())
    print("Documents in transcription_db.test_transcripts:", docs)

if __name__ == "__main__":
    test_mongodb()
