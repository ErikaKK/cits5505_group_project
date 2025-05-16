# Error Handling System

This module provides a comprehensive error handling system for the Flask application, including custom exceptions, error logging, and both JSON and HTML responses.

## Key Features

| Feature | Description |
|---------|-------------|
| Trace ID | Unique identifier for each request to track errors |
| Dual Response | Returns JSON or HTML based on request headers |
| Custom Exceptions | Handles validation, business logic, and rate limiting errors |
| Logging | Detailed error logging with trace IDs |
| Error Templates | HTML templates for user-friendly error pages |

## Error Handlers

| HTTP Code | Type | Description |
|-----------|------|-------------|
| 400 | ValidationError | Input validation failures |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource not found |
| 409 | BusinessError/Conflict | Business logic violations or conflicts |
| 422 | Unprocessable Entity | Invalid request data |
| 429 | TooManyRequestsError | Rate limit exceeded |
| 500 | Internal Server Error | Server-side errors |

## Response Format

### JSON Response
```json
{
    "status_code": 404,
    "trace_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Resource not found",
    "details": "Optional additional information"
}
