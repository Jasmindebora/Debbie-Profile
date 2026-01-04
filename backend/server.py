from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime

from models import (
    ContactSubmissionCreate,
    ContactSubmission,
    ContactSubmissionResponse,
    ErrorResponse
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Dr. Debora Jasmin Portfolio API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Health check endpoint
@api_router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Dr. Debora Jasmin Portfolio API",
        "status": "active",
        "version": "1.0.0"
    }

# Contact form submission endpoint
@api_router.post(
    "/contact",
    response_model=ContactSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def submit_contact_form(submission: ContactSubmissionCreate):
    """
    Submit a contact form message.
    
    - **name**: Name of the person contacting (2-100 chars)
    - **email**: Valid email address
    - **subject**: Subject of the message (3-200 chars)
    - **message**: Message content (10-2000 chars)
    """
    try:
        # Create contact submission object
        contact_data = ContactSubmission(
            name=submission.name,
            email=submission.email,
            subject=submission.subject,
            message=submission.message,
            timestamp=datetime.utcnow(),
            status="new"
        )
        
        # Insert into database
        result = await db.contact_submissions.insert_one(contact_data.dict())
        
        logger.info(f"Contact form submitted by {submission.email}")
        
        return ContactSubmissionResponse(
            success=True,
            message="Message sent successfully. Thank you for reaching out!",
            id=contact_data.id
        )
        
    except Exception as e:
        logger.error(f"Error submitting contact form: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit contact form. Please try again later."
        )

# Get all contact submissions (admin endpoint)
@api_router.get(
    "/contact/submissions",
    response_model=List[ContactSubmission]
)
async def get_contact_submissions(
    limit: int = 50,
    skip: int = 0,
    status_filter: str = None
):
    """
    Get all contact form submissions (Admin endpoint).
    
    - **limit**: Maximum number of submissions to return (default: 50)
    - **skip**: Number of submissions to skip (default: 0)
    - **status_filter**: Filter by status (new, read, replied)
    """
    try:
        # Build query
        query = {}
        if status_filter:
            query["status"] = status_filter
        
        # Fetch submissions
        submissions = await db.contact_submissions.find(
            query,
            {"_id": 0, "id": 1, "name": 1, "email": 1, "subject": 1, "message": 1, "timestamp": 1, "status": 1}
        ).sort("timestamp", -1).skip(skip).limit(limit).to_list(limit)
        
        return [ContactSubmission(**sub) for sub in submissions]
        
    except Exception as e:
        logger.error(f"Error fetching contact submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch contact submissions"
        )

# Get contact submission count
@api_router.get("/contact/count")
async def get_contact_count():
    """Get total count of contact submissions"""
    try:
        total = await db.contact_submissions.count_documents({})
        new = await db.contact_submissions.count_documents({"status": "new"})
        
        return {
            "total": total,
            "new": new,
            "read": total - new
        }
    except Exception as e:
        logger.error(f"Error counting submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get submission count"
        )

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    client.close()
    logger.info("Database connection closed")
