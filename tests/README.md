# EcoFarm Quest Backend Tests

This directory contains comprehensive tests for the EcoFarm Quest Flask backend API.

## Test Structure

### Test Files

- `test_auth.py` - Authentication and authorization tests
- `test_courses.py` - Course management and learning tests
- `test_community.py` - Community features and discussions tests
- `test_users.py` - User profile and settings tests
- `test_achievements.py` - Achievement system tests
- `test_upload.py` - File upload functionality tests
- `test_integration.py` - End-to-end integration tests
- `conftest.py` - Pytest configuration and fixtures

### Test Categories

#### Unit Tests
- Individual API endpoint testing
- Input validation testing
- Error handling testing
- Authentication and authorization testing

#### Integration Tests
- Complete user journey testing
- Cross-module functionality testing
- Data consistency testing
- Error handling workflow testing

## Running Tests

### Prerequisites

1. Install test dependencies:
```bash
pip install pytest pytest-cov pytest-mock
```

2. Set up test environment variables:
```bash
export TESTING=true
export SECRET_KEY=test-secret-key
export JWT_SECRET_KEY=test-jwt-secret-key
export MONGODB_URI=mongodb://localhost:27017/ecofarmquest_test
```

### Running All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run specific test class
pytest tests/test_auth.py::TestAuthAPI

# Run specific test method
pytest tests/test_auth.py::TestAuthAPI::test_register_success
```

### Running Tests by Category

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only authentication tests
pytest -m auth

# Run only course tests
pytest -m courses

# Run only community tests
pytest -m community

# Run only user tests
pytest -m users

# Run only achievement tests
pytest -m achievements

# Run only upload tests
pytest -m upload
```

### Running Tests by Speed

```bash
# Run only fast tests
pytest -m fast

# Run only slow tests
pytest -m slow
```

## Test Configuration

### Pytest Configuration

The `pytest.ini` file contains configuration for:
- Test discovery patterns
- Output formatting
- Markers for test categorization
- Warning handling

### Test Fixtures

The `conftest.py` file provides:
- Test app configuration
- Authentication headers
- Mock objects for testing
- Test data fixtures
- Environment setup/teardown

## Test Data

### Test User Data
- Standard test user for authentication tests
- Mock user objects for unit tests
- Test user data for integration tests

### Test Course Data
- Sample course for testing course functionality
- Mock course objects for unit tests

### Test Achievement Data
- Sample achievement for testing achievement system
- Mock achievement objects for unit tests

### Test Discussion Data
- Sample discussion for testing community features
- Mock discussion objects for unit tests

## Test Coverage

The tests cover:

### Authentication & Authorization
- User registration
- User login/logout
- Token validation
- Password reset
- Protected route access

### User Management
- Profile management
- Settings management
- Avatar updates
- Data export
- Account deletion

### Course Management
- Course browsing
- Course enrollment
- Progress tracking
- Lesson completion
- Quiz submission
- Course search

### Community Features
- Discussion creation
- Discussion replies
- Discussion likes
- Leaderboard management
- Community statistics

### Achievement System
- Achievement browsing
- Achievement unlocking
- Progress tracking
- Achievement statistics
- Leaderboard integration

### File Upload
- Avatar uploads
- Discussion image uploads
- Course thumbnail uploads
- General file uploads
- File validation
- File deletion

### Integration Testing
- Complete user journeys
- Cross-module functionality
- Data consistency
- Error handling workflows

## Mocking

The tests use mocking for:
- Database operations
- JWT token validation
- File upload operations
- External service calls
- Email sending

## Test Database

Tests use a separate test database to avoid affecting production data:
- Database: `ecofarmquest_test`
- Automatic cleanup after each test
- Isolated test data

## Best Practices

### Test Naming
- Test methods start with `test_`
- Descriptive names that explain what is being tested
- Grouped by functionality

### Test Structure
- Setup: Prepare test data and environment
- Execute: Run the code being tested
- Assert: Verify the expected outcome
- Teardown: Clean up test data

### Test Isolation
- Each test is independent
- No shared state between tests
- Proper cleanup after each test

### Error Testing
- Test both success and failure scenarios
- Test edge cases and boundary conditions
- Test error handling and validation

## Continuous Integration

The tests are designed to run in CI/CD pipelines:
- No external dependencies
- Fast execution
- Reliable and repeatable
- Clear pass/fail indicators

## Debugging Tests

### Running Tests in Debug Mode
```bash
# Run with detailed output
pytest -v -s

# Run specific test with debug output
pytest -v -s tests/test_auth.py::TestAuthAPI::test_register_success

# Run with pdb debugger
pytest --pdb
```

### Test Logging
```bash
# Run with logging
pytest --log-cli-level=DEBUG

# Run with specific log level
pytest --log-cli-level=INFO
```

## Performance Testing

### Running Performance Tests
```bash
# Run with timing information
pytest --durations=10

# Run with performance markers
pytest -m performance
```

## Maintenance

### Adding New Tests
1. Create test file following naming convention
2. Add appropriate markers
3. Use existing fixtures when possible
4. Follow test structure guidelines
5. Add to appropriate test category

### Updating Tests
1. Update test data when models change
2. Update mocks when interfaces change
3. Update assertions when behavior changes
4. Maintain test coverage

### Test Documentation
1. Keep test descriptions up to date
2. Document test data requirements
3. Explain complex test scenarios
4. Update this README when adding new test categories
