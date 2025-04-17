import os
import pytest
from fastapi.testclient import TestClient

def test_get_status(test_client: TestClient, test_directories):
    response = test_client.get("/api/v1/admin/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "directories" in data
    assert data["status"] == "running"
    
    # Verify all directories exist
    for dir_name, dir_path in test_directories.items():
        assert dir_name in data["directories"]
        assert os.path.exists(dir_path)

def test_cleanup_system(test_client: TestClient, test_directories):
    # Create test files
    test_files = []
    for dir_name, dir_path in test_directories.items():
        test_file = os.path.join(dir_path, f"test_file_{dir_name}.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        test_files.append(test_file)
    
    # Create a test font file that should not be deleted
    font_file = os.path.join(test_directories["fonts"], "test_font.ttf")
    with open(font_file, "w") as f:
        f.write("test font content")
    
    response = test_client.post("/api/v1/admin/cleanup")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Verify non-font files are deleted
    for test_file in test_files:
        if test_file != font_file:
            assert not os.path.exists(test_file)
    
    # Verify font file still exists
    assert os.path.exists(font_file)
    
    # Cleanup
    if os.path.exists(font_file):
        os.unlink(font_file)

def test_reset_system(test_client: TestClient, test_directories):
    # Create test files and subdirectories
    test_items = []
    for dir_name, dir_path in test_directories.items():
        # Create test file
        test_file = os.path.join(dir_path, f"test_file_{dir_name}.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        test_items.append(test_file)
        
        # Create test subdirectory with a file
        test_subdir = os.path.join(dir_path, f"test_subdir_{dir_name}")
        os.makedirs(test_subdir, exist_ok=True)
        test_items.append(test_subdir)
        
        subdir_file = os.path.join(test_subdir, "test_file.txt")
        with open(subdir_file, "w") as f:
            f.write("test content")
        test_items.append(subdir_file)
    
    response = test_client.post("/api/v1/admin/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Verify directories still exist but are empty
    for dir_path in test_directories.values():
        assert os.path.exists(dir_path)
        assert len(os.listdir(dir_path)) == 0 