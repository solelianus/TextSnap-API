import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import shutil
from PIL import Image
import asyncio
import sys
import warnings
from app.core.config import settings
from app.main import app
import os

# Suppress asyncio-related warnings
warnings.filterwarnings("ignore", message="Exception ignored.*ProactorBasePipeTransport.*")
warnings.filterwarnings("ignore", message="Exception ignored.*_ProactorBasePipeTransport.*")

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
def test_directories():
    """Create and manage test directories."""
    # Define test directories
    test_dirs = {
        "output": settings.OUTPUT_DIR,
        "cache": settings.CACHE_DIR,
        "fonts": settings.FONTS_DIR
    }
    
    # Create test directories if they don't exist
    for dir_path in test_dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    
    yield test_dirs
    
    # Cleanup after tests
    for dir_path in test_dirs.values():
        if os.path.exists(dir_path):
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Error while deleting {item_path}: {e}")

@pytest.fixture
def sample_font(test_directories):
    """Create a sample font file for testing."""
    font_path = os.path.join(test_directories["fonts"], "test_font.ttf")
    with open(font_path, "wb") as f:
        f.write(b"This is a test font file")
    
    yield font_path
    
    # Cleanup
    if os.path.exists(font_path):
        os.unlink(font_path)

@pytest.fixture
def sample_image(test_directories):
    """Create a sample image file for testing."""
    image_path = os.path.join(test_directories["output"], "test_image.png")
    with open(image_path, "wb") as f:
        f.write(b"This is a test image file")
    
    yield image_path
    
    # Cleanup
    if os.path.exists(image_path):
        os.unlink(image_path) 