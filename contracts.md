# Backend Integration Contracts
## Dr. Debora Jasmin Professional Portfolio

### Overview
This document defines the API contracts and integration strategy for the professional portfolio website.

---

## Current Mock Data (frontend/src/mock.js)
- `profileData`: Complete profile information including education, experience, patents, publications, awards, skills, certifications, memberships
- Contact form: Currently shows toast notification on submission (mock)

---

## Backend Implementation Plan

### 1. Database Models

#### Contact Submission Model
```python
{
  "_id": ObjectId,
  "name": str,
  "email": str,
  "subject": str,
  "message": str,
  "timestamp": datetime,
  "status": str (default: "new")  # new, read, replied
}
```

#### Profile Data Model (Optional - for future dynamic content)
```python
{
  "_id": ObjectId,
  "section": str,  # education, experience, patents, publications, etc.
  "data": dict,
  "updated_at": datetime
}
```

---

## 2. API Endpoints

### Contact Form Submission
**Endpoint:** `POST /api/contact`

**Request Body:**
```json
{
  "name": "string",
  "email": "string (email format)",
  "subject": "string",
  "message": "string (min 10 chars)"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Message sent successfully",
  "id": "contact_submission_id"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message"
}
```

### Get Contact Submissions (Admin - Future)
**Endpoint:** `GET /api/contact/submissions`

**Response:**
```json
{
  "success": true,
  "submissions": [
    {
      "id": "string",
      "name": "string",
      "email": "string",
      "subject": "string",
      "message": "string",
      "timestamp": "ISO datetime",
      "status": "string"
    }
  ]
}
```

### Profile Data (Future Enhancement)
**Endpoint:** `GET /api/profile`

**Response:**
```json
{
  "success": true,
  "profile": { /* profile data object */ }
}
```

---

## 3. Frontend Integration Changes

### Files to Update:

#### `/app/frontend/src/components/Contact.jsx`
**Current:** Mock submission with toast notification
**Change to:**
```javascript
// Replace handleSubmit function
const handleSubmit = async (e) => {
  e.preventDefault();
  
  try {
    const response = await axios.post(`${BACKEND_URL}/api/contact`, formData);
    
    if (response.data.success) {
      toast({
        title: "Message Sent!",
        description: "Thank you for reaching out. I'll get back to you soon.",
      });
      setFormData({ name: '', email: '', subject: '', message: '' });
    }
  } catch (error) {
    toast({
      title: "Error",
      description: error.response?.data?.error || "Failed to send message. Please try again.",
      variant: "destructive"
    });
  }
};
```

**Add import:**
```javascript
import axios from 'axios';
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
```

---

## 4. Backend Files to Create/Modify

### Create: `/app/backend/models.py`
- ContactSubmission model using Pydantic
- Validation rules

### Modify: `/app/backend/server.py`
- Import models
- Add contact submission endpoint
- Add get submissions endpoint (admin)
- Error handling

---

## 5. Testing Strategy

### Backend Testing (using deep_testing_backend_v2):
1. Test POST /api/contact with valid data
2. Test POST /api/contact with invalid email
3. Test POST /api/contact with missing fields
4. Test GET /api/contact/submissions
5. Verify MongoDB storage

### Frontend Testing (after user permission):
1. Fill and submit contact form
2. Verify success toast appears
3. Verify form clears after submission
4. Test error handling with invalid data
5. Test form validation

---

## 6. Environment Variables
**No new environment variables needed**
- REACT_APP_BACKEND_URL: Already configured
- MONGO_URL: Already configured

---

## 7. Dependencies
**Backend:**
- All required packages already in requirements.txt
- email-validator (already present)

**Frontend:**
- axios (already installed)

---

## 8. Success Criteria
✅ Contact form submits to backend successfully
✅ Data saved in MongoDB
✅ User receives confirmation toast
✅ Form validation working
✅ Error handling implemented
✅ Backend tests pass
✅ Frontend submission works end-to-end

---

## Notes
- Profile data remains static in mock.js for MVP
- Future enhancement: Admin panel to manage contact submissions
- Future enhancement: Dynamic profile data management
- All mock data stays in place for sections that don't need backend
