# Flas Bot - API Documentation

## Overview

Complete API documentation for Flas Bot. All endpoints require JWT authentication except for auth endpoints.

**Base URL**: `http://localhost:5000/api`

---

## Authentication Endpoints

### Register User

```
POST /auth/users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response (201)**:

```json
{
  "message": "User registered successfully"
}
```

---

### Login

```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response (200)**:

```json
{
  "access_token": "eyJhbGc..."
}
```

---

## Business Endpoints

### Create Business

Create a new business/tenant profile.

```
POST /business/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "business_name": "My Coffee Shop",
  "business_type": "Food & Beverage",
  "description": "Premium coffee shop with specialty drinks",
  "phone": "+1234567890",
  "email": "coffee@example.com",
  "instance_name": "coffee_shop_instance"
}
```

**Response (201)**:

```json
{
  "message": "Business created successfully",
  "business": {
    "id": 1,
    "business_name": "My Coffee Shop",
    "business_type": "Food & Beverage",
    "description": "Premium coffee shop with specialty drinks",
    "phone": "+1234567890",
    "email": "coffee@example.com",
    "instance_name": "coffee_shop_instance"
  }
}
```

---

### Get My Business

Get current user's business information.

```
GET /business/
Authorization: Bearer {access_token}
```

**Response (200)**:

```json
{
  "id": 1,
  "business_name": "My Coffee Shop",
  "business_type": "Food & Beverage",
  "description": "Premium coffee shop with specialty drinks",
  "phone": "+1234567890",
  "email": "coffee@example.com",
  "instance_name": "coffee_shop_instance",
  "created_at": "2024-07-16T10:30:00"
}
```

---

### Update Business

Update business information.

```
PUT /business/{business_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "business_name": "My Premium Coffee Shop",
  "description": "Updated description..."
}
```

**Response (200)**:

```json
{
  "message": "Business updated successfully",
  "business": {
    "id": 1,
    "business_name": "My Premium Coffee Shop",
    "business_type": "Food & Beverage",
    "description": "Updated description...",
    "phone": "+1234567890",
    "email": "coffee@example.com",
    "instance_name": "coffee_shop_instance"
  }
}
```

---

### Delete Business

Delete business profile.

```
DELETE /business/{business_id}
Authorization: Bearer {access_token}
```

**Response (200)**:

```json
{
  "message": "Business deleted successfully"
}
```

---

## Services Endpoints

### Create Service

Add a new service/product to your business.

```
POST /services/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Espresso",
  "description": "Strong, concentrated coffee shot",
  "price": "$3.50"
}
```

**Response (201)**:

```json
{
  "message": "Service created successfully",
  "service": {
    "id": 1,
    "name": "Espresso",
    "description": "Strong, concentrated coffee shot",
    "price": "$3.50"
  }
}
```

---

### List Services

Get all services for the business.

```
GET /services/
Authorization: Bearer {access_token}
```

**Response (200)**:

```json
[
  {
    "id": 1,
    "name": "Espresso",
    "description": "Strong, concentrated coffee shot",
    "price": "$3.50",
    "created_at": "2024-07-16T10:30:00"
  },
  {
    "id": 2,
    "name": "Cappuccino",
    "description": "Espresso with steamed milk",
    "price": "$4.50",
    "created_at": "2024-07-16T10:31:00"
  }
]
```

---

### Update Service

Update service details.

```
PUT /services/{service_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Premium Espresso",
  "price": "$4.00"
}
```

**Response (200)**:

```json
{
  "message": "Service updated successfully",
  "service": {
    "id": 1,
    "name": "Premium Espresso",
    "description": "Strong, concentrated coffee shot",
    "price": "$4.00"
  }
}
```

---

### Delete Service

Delete a service.

```
DELETE /services/{service_id}
Authorization: Bearer {access_token}
```

**Response (200)**:

```json
{
  "message": "Service deleted successfully"
}
```

---

## Knowledge Base Endpoints

### Create Knowledge Entry

Add FAQ or knowledge base information.

```
POST /knowledge/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "How do I place an order?",
  "content": "You can place an order by messaging us on WhatsApp with your order details."
}
```

**Response (201)**:

```json
{
  "message": "Knowledge entry created successfully",
  "knowledge": {
    "id": 1,
    "title": "How do I place an order?",
    "content": "You can place an order by messaging us on WhatsApp with your order details."
  }
}
```

---

### List Knowledge Entries

Get all knowledge base entries.

```
GET /knowledge/
Authorization: Bearer {access_token}
```

**Response (200)**:

```json
[
  {
    "id": 1,
    "title": "How do I place an order?",
    "question": "How do I place an order?",
    "content": "You can place an order by messaging us on WhatsApp...",
    "answer": "You can place an order by messaging us on WhatsApp...",
    "created_at": "2024-07-16T10:30:00"
  }
]
```

---

### Update Knowledge Entry

Update knowledge base information.

```
PUT /knowledge/{knowledge_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Question",
  "content": "Updated answer..."
}
```

**Response (200)**:

```json
{
  "message": "Knowledge entry updated successfully",
  "knowledge": {
    "id": 1,
    "title": "Updated Question",
    "content": "Updated answer..."
  }
}
```

---

### Delete Knowledge Entry

Delete a knowledge base entry.

```
DELETE /knowledge/{knowledge_id}
Authorization: Bearer {access_token}
```

**Response (200)**:

```json
{
  "message": "Knowledge entry deleted successfully"
}
```

---

## Webhook Endpoints

### Receive WhatsApp Messages

Evolution API sends messages to this endpoint.

```
POST /webhook/messages
Content-Type: application/json

{
  "instance_name": "coffee_shop_instance",
  "phone": "+1234567890",
  "message": "Hello, I'd like to place an order"
}
```

**Response (200)**:

```json
{
  "status": "processed",
  "response": {
    "reply": "Hello! Thanks for reaching out...",
    "media": [],
    "follow_up": ""
  }
}
```

---

### Message Status Update

Evolution API sends status updates here.

```
POST /webhook/status
Content-Type: application/json

{
  "messageId": "msg_123",
  "status": "delivered"
}
```

**Response (200)**:

```json
{
  "status": "received"
}
```

---

### General Events

Other Evolution API events.

```
POST /webhook/events
Content-Type: application/json

{
  "event": "connection.update",
  "instance": "coffee_shop_instance"
}
```

**Response (200)**:

```json
{
  "status": "received"
}
```

---

### Webhook Health Check

Check if webhook is running.

```
GET /webhook/health
```

**Response (200)**:

```json
{
  "status": "healthy",
  "service": "flas-webhook",
  "timestamp": "2024-07-16T10:30:00"
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "message": "Missing required fields"
}
```

### 401 Unauthorized

```json
{
  "message": "Missing authorization token"
}
```

### 404 Not Found

```json
{
  "message": "Business not found"
}
```

### 409 Conflict

```json
{
  "message": "User already has a business"
}
```

### 500 Internal Server Error

```json
{
  "message": "Failed to create business: error details"
}
```

---

## Usage Examples

### Example Flow: Complete Setup

1. **Register**

```bash
curl -X POST http://localhost:5000/api/auth/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "password123"
  }'
```

2. **Login**

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

3. **Create Business**

```bash
curl -X POST http://localhost:5000/api/business/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "My Coffee Shop",
    "business_type": "Food & Beverage",
    "description": "Premium coffee shop",
    "phone": "+1234567890",
    "email": "coffee@example.com",
    "instance_name": "coffee_shop"
  }'
```

4. **Add Services**

```bash
curl -X POST http://localhost:5000/api/services/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Espresso",
    "description": "Strong coffee shot",
    "price": "$3.50"
  }'
```

5. **Add Knowledge Base**

```bash
curl -X POST http://localhost:5000/api/knowledge/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "How to order?",
    "content": "Message us on WhatsApp with your order"
  }'
```

---

## Rate Limiting

Currently no rate limiting is implemented. This should be added for production.

---

## Pagination

List endpoints don't currently support pagination. This should be added for production.

---

## Filtering & Sorting

Not currently implemented. Add to list endpoints as needed.

---

## CORS

CORS is enabled for `http://localhost:5173` (Vite dev server).

For production, update in `app/__init__.py`:

```python
CORS(
    app,
    resources={r"/*": {"origins": "https://yourdomain.com"}},
    supports_credentials=True,
)
```

---

## Contact

For API issues or questions, check the logs or contact the development team.
