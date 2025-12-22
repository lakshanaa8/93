## Developer B – Database Work

### CRM Database
- PostgreSQL used for structured CRM data
- Stores patient details, call records, audio file reference
- Acts as the source of truth for calls

### Transcription Database
- MongoDB used for transcription storage
- Stores only converted text from audio
- Linked to CRM via call_id

Bot handling and audio generation is managed separately.
