# MongoDB Architecture Explanation

## Why MongoDB Doesn't Show "Updates" for Call Status

### System Architecture

The system uses a **dual-database architecture** with clear separation of concerns:

#### 1. **PostgreSQL (CRM Database)**
- **Purpose**: Stores structured CRM data
- **Contains**:
  - Patient information
  - Call records (call_id, patient_id, audio_file_url)
  - **Call status** (pending, completed, etc.) ← **This is updated here**
  - Timestamps

#### 2. **MongoDB (Transcription Database)**
- **Purpose**: Stores only transcription text data
- **Contains**:
  - call_id (links to PostgreSQL)
  - transcript_text (the actual transcription)
  - language
  - created_at timestamp
- **Does NOT contain**: Call status, patient info, or other CRM data

### Why This Design?

1. **Separation of Concerns**: 
   - PostgreSQL = Relational, structured data (perfect for CRM)
   - MongoDB = Document store (perfect for flexible text data)

2. **Performance**: 
   - Transcripts can be large text documents
   - MongoDB handles text storage efficiently
   - PostgreSQL handles structured queries efficiently

3. **Scalability**: 
   - Transcripts can grow independently
   - CRM queries don't slow down transcript storage

### What Happens in the Workflow

```
Step 1: Save Call in PostgreSQL
  → Creates call_id (e.g., 39, 40)
  → Status: "pending"

Step 2: Save Transcript in MongoDB
  → Creates NEW document with call_id
  → Stores transcript text
  → MongoDB document is created (not updated)

Step 3: Update Call Status in PostgreSQL
  → Updates call_status to "completed"
  → This happens ONLY in PostgreSQL
  → MongoDB is NOT updated (by design)
```

### Why MongoDB Shows "No Update"?

**MongoDB is working correctly!** Here's why:

1. **MongoDB stores transcripts only** - It doesn't store or track call status
2. **Each transcript is a separate document** - Multiple transcripts can exist for the same call_id
3. **Call status lives in PostgreSQL** - Check PostgreSQL to see status updates

### How to Verify Everything is Working

#### Check PostgreSQL (Call Status):
```sql
SELECT call_id, call_status, created_at 
FROM calls 
WHERE call_id IN (39, 40);
```

#### Check MongoDB (Transcripts):
```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["transcription_db"]
collection = db["transcripts"]

# Find transcripts for call_id 39 and 40
docs = list(collection.find({"call_id": {"$in": [39, 40]}}))
print(f"Found {len(docs)} transcripts")
```

### If You Need to Update Transcripts

If you want to **update an existing transcript** instead of creating a new one, you would need:

```python
# Update existing transcript (upsert pattern)
collection.update_one(
    {"call_id": call_id},
    {"$set": {
        "transcript_text": new_text,
        "updated_at": datetime.now(timezone.utc)
    }},
    upsert=True  # Create if doesn't exist
)
```

But the current design **intentionally creates new documents** each time, which allows:
- Multiple transcript versions
- History tracking
- No data loss

### Summary for Your Sir

**"MongoDB is working correctly. The system uses a dual-database architecture where:**
- **PostgreSQL stores call metadata and status** (this gets updated)
- **MongoDB stores only transcript text** (this gets new documents inserted)
- **Call status updates happen in PostgreSQL, not MongoDB** (by design)
- **This separation allows better performance and scalability**"

The transcripts for call_id 39 and 40 **are being saved in MongoDB** - you can verify by querying MongoDB directly. The "update" you're looking for (call_status) is in PostgreSQL, which is the correct place for it according to the architecture.


