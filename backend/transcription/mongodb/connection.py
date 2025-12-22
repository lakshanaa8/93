from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["transcription_db"]
collection = db["transcripts"]

def save_transcript(call_id, text):
    collection.insert_one({
        "call_id": call_id,
        "transcript_text": text
    })
