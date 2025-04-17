# API Documentation

This document provides detailed information about the TextSnap API endpoints.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

The API uses Bearer token authentication for protected endpoints.

```http
Authorization: Bearer <token>
```

## Endpoints

### Image Generation

#### Generate Image

```http
POST /generate
```

Generates an image from text using the specified font and style.

**Request Body:**
```json
{
    "text": "Hello World",
    "font_name": "arial.ttf",
    "font_size": 24,
    "color": "#000000",
    "background_color": "#FFFFFF",
    "output_format": "png"
}
```

**Parameters:**
- `text` (string, required): Text to render
- `font_name` (string, required): Name of the font file
- `font_size` (integer, optional): Font size in pixels (default: 24)
- `color` (string, optional): Text color in hex (default: "#000000")
- `background_color` (string, optional): Background color in hex (default: "#FFFFFF")
- `output_format` (string, optional): Output format (png/jpg) (default: "png")

**Response:**
- Status: 200 OK
- Content-Type: image/png or image/jpeg
- Body: Binary image data

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello World",
    "font_name": "arial.ttf",
    "font_size": 24,
    "color": "#000000",
    "background_color": "#FFFFFF",
    "output_format": "png"
  }' \
  --output output.png
```

### Font Management

#### List Fonts

```http
GET /fonts
```

Returns a list of available fonts.

**Response:**
```json
{
    "fonts": [
        {
            "name": "arial.ttf",
            "size": 1024,
            "upload_date": "2024-01-01T00:00:00"
        }
    ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/v1/fonts
```

#### Upload Font

```http
POST /fonts/upload
```

Uploads a new font file.

**Request:**
- Content-Type: multipart/form-data
- Parameters:
  - `font_file` (file): Font file (TTF format)
  - `font_name` (string): Name for the font file

**Response:**
```json
{
    "status": "success",
    "message": "Font uploaded successfully",
    "font": {
        "name": "arial.ttf",
        "size": 1024
    }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/fonts/upload \
  -F "font_file=@arial.ttf" \
  -F "font_name=arial.ttf"
```

#### Delete Font

```http
DELETE /fonts/{font_name}
```

Deletes a font file.

**Parameters:**
- `font_name` (string): Name of the font file to delete

**Response:**
```json
{
    "status": "success",
    "message": "Font deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/fonts/arial.ttf
```

### Admin Endpoints

#### System Status

```http
GET /admin/status
```

Returns the current system status.

**Response:**
```json
{
    "status": "running",
    "version": "1.0.0",
    "uptime": "2 days, 3 hours",
    "directories": {
        "output": "/path/to/output",
        "cache": "/path/to/cache",
        "fonts": "/path/to/fonts"
    }
}
```

**Example:**
```bash
curl http://localhost:8000/api/v1/admin/status
```

#### Cleanup System

```http
POST /admin/cleanup
```

Cleans up temporary files and cache.

**Response:**
```json
{
    "status": "success",
    "message": "System cleaned up successfully",
    "cleaned": {
        "files": 10,
        "directories": 2
    }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/admin/cleanup
```

#### Reset System

```http
POST /admin/reset
```

Resets the system to its initial state.

**Response:**
```json
{
    "status": "success",
    "message": "System reset successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/admin/reset
```

## Error Responses

### 400 Bad Request

```json
{
    "detail": "Invalid request parameters"
}
```

### 401 Unauthorized

```json
{
    "detail": "Not authenticated"
}
```

### 403 Forbidden

```json
{
    "detail": "Not authorized"
}
```

### 404 Not Found

```json
{
    "detail": "Resource not found"
}
```

### 422 Unprocessable Entity

```json
{
    "detail": [
        {
            "loc": ["body", "text"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

### 500 Internal Server Error

```json
{
    "detail": "Internal server error"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- 100 requests per minute for unauthenticated users
- 1000 requests per minute for authenticated users

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1609459200
```

## Best Practices

1. **Error Handling**
   - Always check response status codes
   - Handle rate limiting
   - Implement retry logic for 5xx errors

2. **Performance**
   - Use compression for large requests
   - Cache responses when possible
   - Batch operations when available

3. **Security**
   - Use HTTPS for all requests
   - Keep API tokens secure
   - Validate all input data

## SDK Examples

### Python

```python
import requests

class TextSnapClient:
    def __init__(self, base_url="http://localhost:8000/api/v1", token=None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    def generate_image(self, text, font_name, **kwargs):
        data = {
            "text": text,
            "font_name": font_name,
            **kwargs
        }
        response = requests.post(
            f"{self.base_url}/generate",
            json=data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.content

    def list_fonts(self):
        response = requests.get(
            f"{self.base_url}/fonts",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
```

### JavaScript

```javascript
class TextSnapClient {
    constructor(baseUrl = 'http://localhost:8000/api/v1', token = null) {
        this.baseUrl = baseUrl;
        this.headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    }

    async generateImage(text, fontName, options = {}) {
        const response = await fetch(`${this.baseUrl}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...this.headers
            },
            body: JSON.stringify({
                text,
                font_name: fontName,
                ...options
            })
        });
        if (!response.ok) throw new Error('Request failed');
        return response.blob();
    }

    async listFonts() {
        const response = await fetch(`${this.baseUrl}/fonts`, {
            headers: this.headers
        });
        if (!response.ok) throw new Error('Request failed');
        return response.json();
    }
}
```

## Next Steps

- Read the [Development Guide](development.md)
- Check the [Testing Guide](testing.md)
- Learn about [Architecture](architecture.md) 