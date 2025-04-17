# Testing Guide

This guide provides comprehensive information about testing the TextSnap API.

## Test Structure

### Test Organization

```
tests/
├── conftest.py           # Test fixtures and configuration
├── test_generate.py      # Image generation tests
├── test_fonts.py         # Font management tests
└── test_admin.py         # Admin endpoint tests
```

### Test Categories

1. **Unit Tests**
   - Test individual functions and classes
   - Mock external dependencies
   - Focus on business logic

2. **Integration Tests**
   - Test API endpoints
   - Test service interactions
   - Use test database and files

3. **End-to-End Tests**
   - Test complete workflows
   - Use real dependencies
   - Test error scenarios

## Test Fixtures

### Common Fixtures

```python
@pytest.fixture
def test_client():
    """Create a test client for the API."""
    return TestClient(app)

@pytest.fixture
def test_directories():
    """Create temporary directories for testing."""
    dirs = {
        "output": settings.OUTPUT_DIR,
        "cache": settings.CACHE_DIR,
        "fonts": settings.FONTS_DIR
    }
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    yield dirs
    # Cleanup code

@pytest.fixture
def sample_font(test_directories):
    """Create a sample font file for testing."""
    font_path = test_directories["fonts"] / "test.ttf"
    font_path.write_bytes(b"font data")
    return font_path
```

### Using Fixtures

```python
def test_function(test_client, test_directories):
    # Use fixtures in test
    response = test_client.get("/api/v1/status")
    assert response.status_code == 200
```

## Writing Tests

### Test Naming

- Use descriptive names
- Follow `test_` prefix convention
- Include what's being tested

```python
def test_generate_image_with_valid_url():
    # Test code

def test_upload_font_with_invalid_format():
    # Test code
```

### Test Structure

1. **Arrange**
   - Set up test data
   - Configure mocks
   - Prepare environment

2. **Act**
   - Call the function
   - Make the request
   - Perform the action

3. **Assert**
   - Check results
   - Verify side effects
   - Validate responses

### Example Test

```python
def test_generate_image(test_client, sample_image):
    # Arrange
    data = {
        "image_url": "https://example.com/image.jpg",
        "output_format": "png"
    }
    
    # Act
    response = test_client.post("/api/v1/generate", json=data)
    
    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0
```

## Testing API Endpoints

### Response Validation

```python
def test_api_response():
    response = test_client.get("/api/v1/endpoint")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response format
    data = response.json()
    assert "key" in data
    assert isinstance(data["value"], str)
    
    # Check headers
    assert response.headers["content-type"] == "application/json"
```

### Error Handling

```python
def test_error_handling():
    # Test invalid input
    response = test_client.post("/api/v1/endpoint", json={"invalid": "data"})
    assert response.status_code == 422
    
    # Test missing resource
    response = test_client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    
    # Test server error
    response = test_client.post("/api/v1/error")
    assert response.status_code == 500
```

## Testing File Operations

### File Upload

```python
def test_file_upload(test_client):
    # Prepare test file
    test_file = ("test.ttf", b"font data", "application/octet-stream")
    
    # Upload file
    response = test_client.post(
        "/api/v1/fonts/upload",
        files={"font_file": test_file},
        data={"font_name": "test.ttf"}
    )
    
    # Verify upload
    assert response.status_code == 200
    assert Path(settings.FONTS_DIR / "test.ttf").exists()
```

### File Processing

```python
def test_file_processing(test_client, sample_image):
    # Process file
    response = test_client.post(
        "/api/v1/process",
        files={"image": sample_image}
    )
    
    # Verify processing
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
```

## Testing Security

### Input Validation

```python
def test_input_validation():
    # Test path traversal
    response = test_client.get("/api/v1/files/../../etc/passwd")
    assert response.status_code == 400
    
    # Test invalid file types
    response = test_client.post(
        "/api/v1/upload",
        files={"file": ("test.exe", b"malicious", "application/x-msdownload")}
    )
    assert response.status_code == 400
```

### Authentication

```python
def test_authentication():
    # Test unauthorized access
    response = test_client.get("/api/v1/admin")
    assert response.status_code == 401
    
    # Test with valid token
    headers = {"Authorization": "Bearer valid-token"}
    response = test_client.get("/api/v1/admin", headers=headers)
    assert response.status_code == 200
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_generate.py

# Run specific test function
pytest tests/test_generate.py::test_generate_image

# Run with coverage
pytest --cov=app tests/
```

### Test Options

```bash
# Show detailed output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run tests matching pattern
pytest -k "generate"
```

## Continuous Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=app tests/
```

## Best Practices

1. **Test Isolation**
   - Each test should be independent
   - Clean up after tests
   - Don't rely on test order

2. **Test Coverage**
   - Aim for high coverage
   - Focus on critical paths
   - Test edge cases

3. **Test Data**
   - Use realistic data
   - Include edge cases
   - Test invalid inputs

4. **Performance**
   - Keep tests fast
   - Use appropriate fixtures
   - Mock slow operations

## Troubleshooting

### Common Issues

1. **Test Failures**
   - Check error messages
   - Verify test data
   - Review recent changes

2. **Fixture Problems**
   - Check fixture scope
   - Verify cleanup
   - Review dependencies

3. **Environment Issues**
   - Check Python version
   - Verify dependencies
   - Review configuration

### Debugging Tests

```python
def test_debugging():
    # Add print statements
    print("Debug information")
    
    # Use pdb
    import pdb; pdb.set_trace()
    
    # Use pytest's --pdb option
    pytest --pdb
```

## Next Steps

- Read the [Development Guide](development.md)
- Check the [API Documentation](api.md)
- Learn about [Architecture](architecture.md) 