from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving images and CSS/JS)
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/images", StaticFiles(directory=str(static_path / "images")), name="images")
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Models
class PatientSubmission(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    symptoms: str
    message: Optional[str] = None

# Routes
@app.get("/")
async def root():
    return {"message": "PHOENIXIX Medical Bot API"}

@app.get("/api/carousel-images")
async def get_carousel_images():
    """Return the carousel images configuration"""
    return {
        "images": [
            {
                "id": 1,
                "title": "Specialized Medicine",
                "description": "Expert patient and doctor care",
                "url": "/images/slide1_specialized_medicine.jpg"
            },
            {
                "id": 2,
                "title": "Your Health Is Our Priority",
                "description": "Comprehensive healthcare for you and your family",
                "url": "/images/slide2_health_priority.jpg"
            },
            {
                "id": 3,
                "title": "Exceptional Service",
                "description": "Top quality medical consultation",
                "url": "/images/slide3_exceptional_service.jpg"
            }
        ]
    }

@app.post("/api/submit")
async def submit_patient_info(submission: PatientSubmission):
    """
    Handle patient submission and trigger bot call
    """
    try:
        # Validate required fields
        if not submission.name or not submission.phone:
            raise HTTPException(status_code=400, detail="Name and phone are required")
        
        # Here you would integrate with your bot calling service
        # For now, we'll simulate the call
        bot_response = await call_medical_bot(
            patient_name=submission.name,
            phone_number=submission.phone,
            email=submission.email,
            symptoms=submission.symptoms,
            message=submission.message
        )
        
        return {
            "status": "success",
            "message": "Form submitted successfully. The medical bot will call you shortly.",
            "call_id": bot_response.get("call_id"),
            "patient_name": submission.name,
            "phone": submission.phone
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Submission failed: {str(e)}")

async def call_medical_bot(patient_name: str, phone_number: str, email: Optional[str], symptoms: str, message: Optional[str]):
    """
    Trigger the medical bot to call the patient
    This is where you integrate with your bot service
    """
    try:
        # TODO: Integrate with your actual bot calling service
        # For now, return a mock response
        return {
            "status": "success",
            "call_id": f"CALL_{patient_name.replace(' ', '_')}_{phone_number}",
            "message": "Bot call initiated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bot call failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

