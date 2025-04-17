# Development Guide

This guide provides information for developers who want to contribute to the TextSnap API project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment (recommended)
- Code editor (VS Code, PyCharm, etc.)

### Initial Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/solelianus/textsnap-api.git
   cd textsnap-api
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

### Development Tools

1. **Code Formatting**
   - Black for code formatting
   - isort for import sorting
   ```bash
   black .
   isort .
   ```

2. **Linting**
   - flake8 for code style checking
   ```bash
   flake8
   ```

3. **Type Checking**
   - mypy for static type checking
   ```bash
   mypy app tests
   ```

4. **Testing**
   - pytest for running tests
   - pytest-cov for coverage reporting
   ```bash
   pytest --cov=app tests/
   ```

## Project Structure

```
textsnap-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── generate.py
│   │       │   ├── fonts.py
│   │       │   └── admin.py
│   │       └── router.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   │   └── request.py
│   ├── services/
│   │   ├── image_processor.py
│   │   ├── font_manager.py
│   │   └── svg_processor.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_generate.py
│   ├── test_fonts.py
│   └── test_admin.py
├── docs/
└── requirements.txt
```

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all public functions and classes
- Keep functions small and focused

### Documentation

- Update README.md for major changes
- Document new features in docs/
- Add docstrings to all new code
- Update API documentation for new endpoints

### Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Include both unit and integration tests
- Test edge cases and error conditions

## Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run Tests and Checks**
   ```bash
   # Run tests
   pytest
   
   # Check code style
   flake8
   
   # Check types
   mypy app tests
   
   # Format code
   black .
   isort .
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push Changes**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Create PR on GitHub
   - Add description of changes
   - Link related issues
   - Request review

## Contributing Guidelines

### Pull Requests

1. **Branch Naming**
   - `feature/` for new features
   - `fix/` for bug fixes
   - `docs/` for documentation
   - `refactor/` for code refactoring

2. **Commit Messages**
   - Use present tense
   - Start with type: feat, fix, docs, style, refactor, test, chore
   - Keep it concise but descriptive

3. **Code Review**
   - Address all review comments
   - Keep PRs focused and small
   - Update documentation as needed

### Issue Reporting

1. **Bug Reports**
   - Describe the bug
   - Include steps to reproduce
   - Add error messages
   - Specify environment

2. **Feature Requests**
   - Describe the feature
   - Explain the use case
   - Suggest implementation
   - Consider alternatives

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_generate.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Writing Tests

1. **Unit Tests**
   ```python
   def test_function():
       # Arrange
       input = "test"
       
       # Act
       result = process(input)
       
       # Assert
       assert result == expected
   ```

2. **Integration Tests**
   ```python
   def test_endpoint(test_client):
       response = test_client.post("/api/v1/generate", json=data)
       assert response.status_code == 200
   ```

3. **Fixtures**
   ```python
   @pytest.fixture
   def test_data():
       return {
           "image_url": "https://example.com/image.jpg",
           "output_format": "png"
       }
   ```

## Performance Considerations

1. **Image Processing**
   - Use async operations
   - Implement caching
   - Optimize memory usage
   - Handle large files

2. **API Endpoints**
   - Implement rate limiting
   - Use efficient algorithms
   - Cache responses
   - Handle errors gracefully

## Security

1. **Input Validation**
   - Validate all inputs
   - Sanitize file paths
   - Check file types
   - Limit file sizes

2. **Error Handling**
   - Don't expose sensitive information
   - Log errors properly
   - Handle edge cases
   - Implement timeouts

## Deployment

### Local Development

```bash
# Start development server
python -m app.main
```

### Production

1. **Environment Setup**
   ```bash
   # Set environment variables
   export ENV=production
   export SECRET_KEY=your-secret-key
   ```

2. **Start Server**
   ```bash
   # Using uvicorn
   uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```

## Next Steps

- Read the [API Documentation](api.md)
- Check the [Testing Guide](testing.md)
- Learn about [Architecture](architecture.md) 