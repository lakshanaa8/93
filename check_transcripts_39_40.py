"""Check transcripts for call_id 39 and 40"""
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["transcription_db"]
collection = db["transcripts"]

print("=" * 60)
print("Checking transcripts for call_id 39 and 40")
print("=" * 60)

docs = list(collection.find({"call_id": {"$in": [39, 40]}}))
print(f"\nFound {len(docs)} document(s) for call_id 39 and 40\n")

for doc in docs:
    print(f"call_id: {doc['call_id']}")
    print(f"MongoDB _id: {doc['_id']}")
    print(f"transcript_text: {doc['transcript_text']}")
    print(f"language: {doc.get('language', 'N/A')}")
    print(f"created_at: {doc.get('created_at', 'N/A')}")
    print("-" * 60)

if len(docs) == 0:
    print("No transcripts found for call_id 39 or 40")
    print("This means MongoDB insertions may have failed silently")

