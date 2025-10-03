"""
Unit tests for Forms
"""
import pytest
from forms import ProductForm, CategoryForm, StockMovementForm, ReportForm
from datetime import date


class TestProductForm:
    """Test ProductForm validation"""
    
    def test_valid_product_form(self, client):
        """Test valid product form"""
        form_data = {
            'name': 'Test Product',
            'barcode': '1234567890',
            'price': 29.99,
            'stock': 100,
            'min_stock': 10,
            'category_id': 1
        }
        
        form = ProductForm(data=form_data)
        form.category_id.choices = [(1, 'Test Category')]
        
        assert form.validate() is True
    
    def test_product_form_missing_name(self, client):
        """Test product form with missing name"""
        form_data = {
            'barcode': '1234567890',
            'price': 29.99,
            'stock': 100,
            'min_stock': 10,
            'category_id': 1
        }
        
        form = ProductForm(data=form_data)
        form.category_id.choices = [(1, 'Test Category')]
        
        assert form.validate() is False
        assert 'This field is required.' in form.name.errors
    
    def test_product_form_invalid_price(self, client):
        """Test product form with invalid price"""
        form_data = {
            'name': 'Test Product',
            'barcode': '1234567890',
            'price': -10.0,  # Negative price
            'stock': 100,
            'min_stock': 10,
            'category_id': 1
        }
        
        form = ProductForm(data=form_data)
        form.category_id.choices = [(1, 'Test Category')]
        
        assert form.validate() is False
        assert 'Number must be at least 0.' in form.price.errors
    
    def test_product_form_long_name(self, client):
        """Test product form with too long name"""
        form_data = {
            'name': 'A' * 101,  # 101 characters, max is 100
            'price': 29.99,
            'stock': 100,
            'min_stock': 10,
            'category_id': 1
        }
        
        form = ProductForm(data=form_data)
        form.category_id.choices = [(1, 'Test Category')]
        
        assert form.validate() is False
        assert 'Field must be between 2 and 100 characters long.' in form.name.errors
    
    def test_product_form_optional_barcode(self, client):
        """Test product form with optional barcode"""
        form_data = {
            'name': 'Test Product',
            'price': 29.99,
            'stock': 100,
            'min_stock': 10,
            'category_id': 1
        }
        
        form = ProductForm(data=form_data)
        form.category_id.choices = [(1, 'Test Category')]
        
        assert form.validate() is True
        assert form.barcode.data is None or form.barcode.data == ''


class TestCategoryForm:
    """Test CategoryForm validation"""
    
    def test_valid_category_form(self, client):
        """Test valid category form"""
        form_data = {
            'name': 'Test Category',
            'description': 'This is a test category'
        }
        
        form = CategoryForm(data=form_data)
        assert form.validate() is True
    
    def test_category_form_missing_name(self, client):
        """Test category form with missing name"""
        form_data = {
            'description': 'This is a test category'
        }
        
        form = CategoryForm(data=form_data)
        assert form.validate() is False
        assert 'This field is required.' in form.name.errors
    
    def test_category_form_short_name(self, client):
        """Test category form with too short name"""
        form_data = {
            'name': 'A',  # 1 character, min is 2
            'description': 'This is a test category'
        }
        
        form = CategoryForm(data=form_data)
        assert form.validate() is False
        assert 'Field must be between 2 and 50 characters long.' in form.name.errors
    
    def test_category_form_long_description(self, client):
        """Test category form with too long description"""
        form_data = {
            'name': 'Test Category',
            'description': 'A' * 201  # 201 characters, max is 200
        }
        
        form = CategoryForm(data=form_data)
        assert form.validate() is False
        assert 'Field cannot be longer than 200 characters.' in form.description.errors
    
    def test_category_form_optional_description(self, client):
        """Test category form with optional description"""
        form_data = {
            'name': 'Test Category'
        }
        
        form = CategoryForm(data=form_data)
        assert form.validate() is True


class TestStockMovementForm:
    """Test StockMovementForm validation"""
    
    def test_valid_stock_movement_form(self, client):
        """Test valid stock movement form"""
        form_data = {
            'product_id': 1,
            'type': 'inflow',
            'amount': 50,
            'description': 'Restocking'
        }
        
        form = StockMovementForm(data=form_data)
        form.product_id.choices = [(1, 'Test Product')]
        
        assert form.validate() is True
    
    def test_stock_movement_form_missing_product(self, client):
        """Test stock movement form with missing product"""
        form_data = {
            'type': 'inflow',
            'amount': 50,
            'description': 'Restocking'
        }
        
        form = StockMovementForm(data=form_data)
        form.product_id.choices = [(1, 'Test Product')]
        
        assert form.validate() is False
        assert 'This field is required.' in form.product_id.errors
    
    def test_stock_movement_form_invalid_type(self, client):
        """Test stock movement form with invalid type"""
        form_data = {
            'product_id': 1,
            'type': 'invalid_type',
            'amount': 50,
            'description': 'Restocking'
        }
        
        form = StockMovementForm(data=form_data)
        form.product_id.choices = [(1, 'Test Product')]
        
        assert form.validate() is False
        assert 'Not a valid choice' in form.type.errors
    
    def test_stock_movement_form_zero_amount(self, client):
        """Test stock movement form with zero amount"""
        form_data = {
            'product_id': 1,
            'type': 'inflow',
            'amount': 0,  # Invalid, must be >= 1
            'description': 'Restocking'
        }
        
        form = StockMovementForm(data=form_data)
        form.product_id.choices = [(1, 'Test Product')]
        
        assert form.validate() is False
        assert 'Number must be at least 1.' in form.amount.errors
    
    def test_stock_movement_form_optional_description(self, client):
        """Test stock movement form with optional description"""
        form_data = {
            'product_id': 1,
            'type': 'outflow',
            'amount': 10
        }
        
        form = StockMovementForm(data=form_data)
        form.product_id.choices = [(1, 'Test Product')]
        
        assert form.validate() is True


class TestReportForm:
    """Test ReportForm validation"""
    
    def test_valid_report_form(self, client):
        """Test valid report form"""
        form_data = {
            'starting_date': date(2023, 1, 1),
            'ending_date': date(2023, 12, 31),
            'category_id': '1'
        }
        
        form = ReportForm(data=form_data)
        form.category_id.choices = [('', 'All Categories'), ('1', 'Test Category')]
        
        assert form.validate() is True
    
    def test_report_form_missing_dates(self, client):
        """Test report form with missing dates"""
        form_data = {
            'category_id': '1'
        }
        
        form = ReportForm(data=form_data)
        form.category_id.choices = [('', 'All Categories'), ('1', 'Test Category')]
        
        assert form.validate() is False
        assert 'This field is required.' in form.starting_date.errors
        assert 'This field is required.' in form.ending_date.errors
    
    def test_report_form_optional_category(self, client):
        """Test report form with optional category"""
        form_data = {
            'starting_date': date(2023, 1, 1),
            'ending_date': date(2023, 12, 31),
            'category_id': ''  # Empty string for all categories
        }
        
        form = ReportForm(data=form_data)
        form.category_id.choices = [('', 'All Categories'), ('1', 'Test Category')]
        
        assert form.validate() is True
    
    def test_report_form_invalid_date_range(self, client):
        """Test report form with end date before start date"""
        # Note: This validation would need to be added to the form
        # as a custom validator if we want to check date ranges
        form_data = {
            'starting_date': date(2023, 12, 31),
            'ending_date': date(2023, 1, 1),  # End before start
            'category_id': '1'
        }
        
        form = ReportForm(data=form_data)
        form.category_id.choices = [('', 'All Categories'), ('1', 'Test Category')]
        
        # Currently, this will validate as True since we don't have 
        # date range validation in the form
        assert form.validate() is True