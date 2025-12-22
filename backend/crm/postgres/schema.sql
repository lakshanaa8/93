CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE calls (
    call_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    audio_file_url TEXT,
    call_status VARCHAR(20), -- hot / non-hot
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
