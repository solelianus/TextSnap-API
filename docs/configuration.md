# Configuration Guide

This guide explains all configuration options available in the TextSnap API.

## Environment Variables

All configuration is done through environment variables, which can be set in a `.env` file or directly in the environment.

### API Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `API_V1_STR` | string | `/api/v1` | Base path for API endpoints |
| `PROJECT_NAME` | string | `TextSnap API` | Name of the project |

### Server Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HOST` | string | `0.0.0.0` | Host to bind the server to |
| `PORT` | int | `8080` | Port to run the server on |
| `RELOAD` | bool | `false` | Enable auto-reload for development |

### Security Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SECRET_KEY` | string | - | Secret key for JWT token generation |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | `30` | Token expiration time in minutes |

### Rate Limiting

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `RATE_LIMIT_PER_MINUTE` | int | `60` | Maximum requests per minute per IP |

### Logging

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LOG_LEVEL` | string | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `LOG_FORMAT` | string | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` | Log message format |

## Directory Configuration

The following directories are used by the application:

| Directory | Purpose | Default Location |
|-----------|---------|------------------|
| `FONTS_DIR` | Font files | `assets/fonts` |
| `OUTPUT_DIR` | Generated images | `output` |
| `CACHE_DIR` | Temporary files | `cache` |
| `LOGS_DIR` | Log files | `logs` |

## Image Processing Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MAX_IMAGE_SIZE` | int | `10485760` | Maximum image size in bytes (10MB) |
| `ALLOWED_IMAGE_FORMATS` | list | `["png", "jpg", "jpeg", "webp"]` | Supported input formats |
| `ALLOWED_OUTPUT_FORMATS` | list | `["png", "jpg", "jpeg", "webp", "pdf"]` | Supported output formats |

## Example Configuration

```env
# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=TextSnap API

# Server Settings
HOST=0.0.0.0
PORT=8080
RELOAD=false

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Image Processing
MAX_IMAGE_SIZE=10485760
ALLOWED_IMAGE_FORMATS=["png", "jpg", "jpeg", "webp"]
ALLOWED_OUTPUT_FORMATS=["png", "jpg", "jpeg", "webp", "pdf"]
```

## Best Practices

1. **Security**
   - Always set a strong `SECRET_KEY` in production
   - Use HTTPS in production
   - Implement proper rate limiting

2. **Performance**
   - Adjust `RATE_LIMIT_PER_MINUTE` based on your server capacity
   - Monitor `MAX_IMAGE_SIZE` to prevent memory issues
   - Use appropriate logging levels

3. **Development**
   - Set `RELOAD=true` during development
   - Use `LOG_LEVEL=DEBUG` for detailed logging
   - Test with different image formats

## Troubleshooting

### Common Configuration Issues

1. **Invalid Environment Variables**
   ```bash
   # Check if all required variables are set
   python -c "from app.core.config import settings; print(settings.dict())"
   ```

2. **Directory Permissions**
   ```bash
   # Fix directory permissions
   chmod -R 755 assets output cache logs
   ```

3. **Rate Limiting Issues**
   - Check if `RATE_LIMIT_PER_MINUTE` is set too low
   - Monitor server logs for rate limit errors

## Next Steps

- Read the [Architecture Documentation](architecture.md)
- Check the [API Documentation](api.md)
- Learn about [Testing](testing.md) 