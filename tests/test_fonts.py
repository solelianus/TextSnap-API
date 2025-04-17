import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from app.core.config import settings
import os

def test_list_fonts(test_client: TestClient, sample_font):
    # Make request
    response = test_client.get("/api/v1/fonts/list")
    
    # Assertions
    assert response.status_code == 200
    assert "fonts" in response.json()
    assert isinstance(response.json()["fonts"], list)
    # Check for the font name without extension
    assert "test_font" in response.json()["fonts"]

def test_upload_font(test_client: TestClient, test_directories):
    font_path = os.path.join(test_directories["fonts"], "new_font.ttf")
    with open(font_path, "wb") as f:
        f.write(b"This is a test font file")
    
    with open(font_path, "rb") as f:
        response = test_client.post(
            "/api/v1/fonts/upload",
            files={"font_file": ("new_font.ttf", f, "application/octet-stream")},
            data={"font_name": "new_font.ttf"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(os.path.join(settings.FONTS_DIR, "new_font.ttf"))
    
    # Cleanup
    if os.path.exists(font_path):
        os.unlink(font_path)

def test_delete_font(test_client: TestClient, sample_font):
    # Get the font name from the path
    font_name = os.path.basename(sample_font)
    
    # Make request
    response = test_client.delete(f"/api/v1/fonts/{font_name}")
    
    # Assertions
    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()
    assert response.json()["status"] == "success"
    
    # Verify file was deleted
    assert not os.path.exists(sample_font)

def test_delete_nonexistent_font(test_client: TestClient):
    # Make request
    response = test_client.delete("/api/v1/fonts/nonexistent_font")
    
    # Assertions
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "Font not found" in response.json()["detail"] 