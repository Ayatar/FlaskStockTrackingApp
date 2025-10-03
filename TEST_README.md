# Flask Stock Tracking System - Test Documentation

## Test Structure

The test suite is organized into several modules:

### Test Modules

1. **`test_models.py`** - Unit tests for database models
   - Category model tests
   - Product model tests  
   - StockMovement model tests
   - Model relationship tests

2. **`test_forms.py`** - Form validation tests
   - ProductForm validation
   - CategoryForm validation
   - StockMovementForm validation
   - ReportForm validation

3. **`test_routes.py`** - Integration tests for Flask routes
   - Dashboard routes
   - Product CRUD routes
   - Category CRUD routes
   - Stock movement routes
   - Analytics routes
   - Report routes
   - Export functionality
   - Error handling

4. **`test_performance.py`** - Performance and load tests
   - Page load time tests
   - Database query performance
   - Concurrent request handling
   - Large data export tests
   - Security tests

5. **`run_tests.py`** - Simple test runner using unittest
   - Can run without pytest installation
   - Provides detailed test summary

## Running Tests

### Option 1: Using pytest (Recommended)

1. Install test dependencies:
```bash
pip install -r test_requirements.txt
```

2. Run all tests:
```bash
pytest
```

3. Run specific test modules:
```bash
pytest tests/test_models.py
pytest tests/test_routes.py
```

4. Run tests with coverage:
```bash
pytest --cov=. --cov-report=html
```

5. Run only fast tests:
```bash
pytest -m "not slow"
```

### Option 2: Using built-in test runner

```bash
python tests/run_tests.py
```

## Test Configuration

### Test Database
- Uses SQLite in-memory database for isolation
- Fresh database created for each test
- Test data automatically created and cleaned up

### Test Data
The test suite creates the following test data:
- **Categories**: Electronics, Clothing, Books
- **Products**: 
  - Laptop (normal stock)
  - T-Shirt (critical stock)
  - Python Book (no barcode)
- **Stock Movements**: Sample inflow/outflow movements

### Test Coverage

The test suite covers:

#### Models (test_models.py)
- ✅ Model creation and validation
- ✅ Model relationships
- ✅ Business logic (critical stock calculation)
- ✅ Database constraints
- ✅ Model string representations

#### Forms (test_forms.py)
- ✅ Form validation (required fields)
- ✅ Data type validation
- ✅ Length constraints
- ✅ Number range validation
- ✅ Optional field handling

#### Routes (test_routes.py)
- ✅ GET requests for all pages
- ✅ POST requests for CRUD operations
- ✅ Form submissions
- ✅ File exports (Excel, PDF)
- ✅ Search and filtering
- ✅ Error handling (404, validation errors)
- ✅ Success/failure flows

#### Performance (test_performance.py)
- ✅ Page load times
- ✅ Database query performance
- ✅ Concurrent request handling
- ✅ Large data processing
- ✅ Export performance
- ✅ Security (SQL injection, XSS)
- ✅ Input validation
- ✅ Data integrity

## Test Results and Reports

### HTML Coverage Report
After running `pytest --cov=. --cov-report=html`, open `htmlcov/index.html` to view detailed coverage report.

### Test Report
HTML test report is generated at `test_reports/report.html` with detailed results.

### Console Output
- Test progress and results
- Coverage percentage
- Failed test details
- Performance metrics

## Writing New Tests

### Test Class Structure
```python
class TestNewFeature(BaseTestCase):
    """Test new feature"""
    
    def test_feature_functionality(self):
        """Test specific functionality"""
        # Arrange
        # Act  
        # Assert
```

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Use descriptive names that explain what is being tested

### Test Categories
Use pytest markers to categorize tests:
```python
@pytest.mark.slow
def test_large_export():
    """Test that takes longer to run"""
    pass

@pytest.mark.integration  
def test_full_workflow():
    """Test that spans multiple components"""
    pass
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Arrange-Act-Assert**: Structure tests clearly
3. **Descriptive Names**: Test names should explain the scenario
4. **Test Data**: Use minimal, focused test data
5. **Cleanup**: Tests should clean up after themselves
6. **Coverage**: Aim for high coverage but focus on critical paths
7. **Performance**: Mark slow tests appropriately
8. **Documentation**: Document complex test scenarios

## Continuous Integration

To integrate with CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r test_requirements.txt
    pytest --cov=. --cov-report=xml
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure project root is in Python path
2. **Database Errors**: Check test database configuration
3. **Fixture Issues**: Verify fixture dependencies
4. **Slow Tests**: Use markers to skip slow tests during development

### Debug Mode
Run tests with verbose output:
```bash
pytest -v -s
```

### Failed Test Investigation
```bash
pytest --tb=long  # Detailed traceback
pytest --pdb      # Drop into debugger on failure
```