import pytest
from fastapi.testclient import TestClient
import os
from pathlib import Path
from app.core.config import settings

def test_generate_image(test_client: TestClient, sample_image):
    # Test data with Lorem Picsum image
    test_data = {
        "image_url": "https://picsum.photos/200/300",
        "output_format": "png",
        "items": [
            {
                "text": "Test Text",
                "position": [50, 50],
                "font_family": "Arial",
                "font_size": 24,
                "color": "#000000"
            }
        ],
        "font_family": "Arial"
    }
    
    # Make request
    response = test_client.post("/api/v1/generate/", json=test_data)
    
    # Assertions
    assert response.status_code == 200
    assert "status" in response.json()
    assert "download_url" in response.json()
    assert response.json()["status"] == "success"
    
    # Verify file was created
    filename = response.json()["download_url"].split("/")[-1]
    assert (settings.OUTPUT_DIR / filename).exists()

def test_generate_image_with_custom_text(test_client: TestClient):
    # Test data with custom text and styling
    test_data = {
        "image_url": "https://picsum.photos/200/300",
        "output_format": "png",
        "items": [
            {
                "text": "Custom Overlay",
                "position": [100, 100],
                "font_family": "Arial",
                "font_size": 32,
                "color": "#FF0000",
                "font_weight": "bold",
                "font_style": "italic"
            }
        ],
        "font_family": "Arial"
    }
    
    # Make request
    response = test_client.post("/api/v1/generate/", json=test_data)
    
    # Assertions
    assert response.status_code == 200
    assert "status" in response.json()
    assert "download_url" in response.json()
    assert response.json()["status"] == "success"
    
    # Verify file was created
    filename = response.json()["download_url"].split("/")[-1]
    assert (settings.OUTPUT_DIR / filename).exists()

def test_generate_image_invalid_url(test_client: TestClient):
    # Test data with invalid URL
    test_data = {
        "image_url": "not_a_valid_url",
        "output_format": "png",
        "items": [
            {
                "text": "Test Text",
                "position": [50, 50],
                "font_family": "Arial",
                "font_size": 24,
                "color": "#000000"
            }
        ],
        "font_family": "Arial"
    }
    
    # Make request
    response = test_client.post("/api/v1/generate/", json=test_data)
    
    # Assertions
    assert response.status_code == 422  # FastAPI validation error
    assert "detail" in response.json()
    assert any("Input should be a valid URL" in error.get("msg", "") for error in response.json()["detail"]) 