# Installation Guide

This guide provides detailed instructions for installing and setting up the TextSnap API.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Git (for version control)
- Virtual environment (recommended)

## System Requirements

### Minimum Requirements
- CPU: 2 cores
- RAM: 2GB
- Storage: 1GB free space
- OS: Windows 10/11, macOS 10.15+, or Linux

### Recommended Requirements
- CPU: 4 cores
- RAM: 4GB
- Storage: 2GB free space
- OS: Latest stable version

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/textsnap-api.git
cd textsnap-api
```

### 2. Create Virtual Environment

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

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
```

### 5. Create Required Directories

```bash
mkdir -p assets/fonts output cache logs
```

### 6. Start the Server

```bash
python -m app.main
```

## Verification

To verify the installation:

1. Open your browser and navigate to `http://localhost:8080/api/v1/docs`
2. You should see the Swagger UI documentation
3. Try the `/api/v1/fonts/list` endpoint to verify the API is working

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find the process using the port
   lsof -i :8080  # macOS/Linux
   netstat -ano | findstr :8080  # Windows
   
   # Kill the process
   kill <PID>  # macOS/Linux
   taskkill /PID <PID> /F  # Windows
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Permission Issues**
   ```bash
   # Fix directory permissions
   chmod -R 755 assets output cache logs
   ```

## Next Steps

- Read the [Configuration Guide](configuration.md)
- Check out the [API Documentation](api.md)
- Learn about [Development Setup](development.md) 