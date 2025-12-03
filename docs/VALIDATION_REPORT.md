# Stake Input Validation Implementation Report

## Overview
This document describes the implementation of input validation for the "stake" (count/quantity) field in the Royal Japan e-commerce application. The validation is implemented on both frontend and backend to ensure data integrity and provide a good user experience.

## Implementation Summary

### Frontend Changes
**File Modified:** `frontend/src/app/order/testcomp.js`

**Changes Made:**
1. Added `countError` state to track validation errors
2. Implemented `useEffect` hook to validate count on page load
3. Added client-side validation in the form submission handler
4. Display inline error message in Japanese when validation fails
5. Parse and send count as integer in POST request

**Validation Rules:**
- Count must be a valid number
- Count must be greater than 0
- Error message: "数量は1以上の正の整数である必要があります。" (Quantity must be a positive integer greater than or equal to 1)

### Backend Changes
**File Modified:** `backend/royal/api/views.py`

**Changes Made:**
1. Updated `CreatePaymentIntentView.post()` method with validation
2. Updated `CompletePayment.post()` method with validation
3. Return HTTP 400 Bad Request with helpful JSON error message when validation fails

**Validation Rules:**
- Count must be present in request data
- Count must be convertible to integer
- Count must be greater than 0
- Error response format:
```json
{
  "errors": {
    "count": "数量は1以上の正の整数である必要があります。"
  },
  "status code": 400
}
```

## Testing

### Frontend Testing

**Setup Steps:**

1. Run database migrations:
```bash
cd backend
python backend/manage.py migrate
```

2. Create test data using the helper script `backend/scripts/get_test_ids.py`:
```bash
python scripts/get_test_ids.py
```

This script creates a test user and product, then outputs their IDs for testing.

3. Start the frontend development server:
```bash
cd frontend
npm run dev
```

4. Start the backend server:
```bash
cd backend
python manage.py runserver
```

**Test Scenario:**

Navigate to the order page with an invalid count parameter:
```
http://localhost:3000/order/<USER_ID>/<PRODUCT_ID>?count=-5
```

Or with a non-numeric value:
```
http://localhost:3000/order/<USER_ID>/<PRODUCT_ID>?count=abc
```

**Expected Result:**
- Error message appears immediately on page load
- Error message is displayed in red at the top of the form in step 1
- User cannot proceed to step 2 when clicking "次へ" (Next) button

**Screenshot:**
![Frontend Validation Error](https://i.imgur.com/rqD3HnL.png)

---

### Backend Testing

The backend validation was tested using curl commands to send direct POST requests with invalid payloads.

**Test 1: Invalid Count - Non-numeric Value**

Command:
```bash
curl -X POST 'http://localhost:8000/api/create-payment-intent' \
  -H 'Content-Type: application/json' \
  -d '{"product":"1","coupon":"","count":"abc"}' -i
```

Expected Response:
- HTTP Status: `400 Bad Request`
- Response Body:
```json
{
  "errors": {
    "count": "数量は1以上の正の整数である必要があります。"
  },
  "status code": 400
}
```

**Test 2: Invalid Count - Zero or Negative Value**

Command:
```bash
curl -X POST 'http://localhost:8000/api/sold' \
  -H 'Content-Type: application/json' \
  -d '{"product":"1","user":"<USER_ID>","coupon":"","count":0,"email":"test@test.com","name":"Test","phone":"123","address":"Addr","address1":"Addr1"}' -i
```

Expected Response:
- HTTP Status: `400 Bad Request`
- Response Body:
```json
{
  "errors": {
    "count": "数量は1以上の正の整数である必要があります。"
  },
  "status code": 400
}
```

---

## Technical Details

### Affected Endpoints
1. `POST /api/create-payment-intent` - Payment intent creation
2. `POST /api/sold` - Order completion

### Error Handling Flow
1. **Frontend validation (first line of defense):**
   - Validates on page load via useEffect
   - Validates before form submission
   - Shows inline error message
   - Prevents invalid data from being sent to server

2. **Backend validation (security layer):**
   - Validates all incoming requests
   - Returns structured error response
   - Prevents invalid data from reaching database

## Conclusion

The implementation successfully adds comprehensive validation for the stake/count input field across both frontend and backend layers. This ensures:
- Better user experience with immediate feedback
- Data integrity at the API level
- Prevention of invalid orders
- Clear, localized error messages in Japanese for end users