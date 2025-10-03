"""
Test runner script
Run all tests for Flask Stock Tracking System
"""
import os
import sys
import unittest
import sqlite3
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import app and models after path setup
from app import app, db
from models import Product, Category, StockMovement


class TestConfig:
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    WTF_CSRF_ENABLED = False


class BaseTestCase(unittest.TestCase):
    """Base test case with setup and teardown"""
    
    def setUp(self):
        """Set up test environment"""
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.create_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def create_test_data(self):
        """Create test data"""
        # Create categories
        self.category1 = Category(name='Electronics', description='Electronic products')
        self.category2 = Category(name='Clothing', description='Clothing items')
        self.category3 = Category(name='Books', description='Books and literature')
        
        db.session.add_all([self.category1, self.category2, self.category3])
        db.session.commit()
        
        # Create products
        self.product1 = Product(
            name='Laptop',
            barcode='123456789',
            price=999.99,
            stock=15,
            min_stock=5,
            category_id=self.category1.id
        )
        
        self.product2 = Product(
            name='T-Shirt',
            barcode='987654321',
            price=29.99,
            stock=3,  # Critical stock
            min_stock=10,
            category_id=self.category2.id
        )
        
        self.product3 = Product(
            name='Python Book',
            price=49.99,
            stock=25,
            min_stock=5,
            category_id=self.category3.id
        )
        
        db.session.add_all([self.product1, self.product2, self.product3])
        db.session.commit()
        
        # Create stock movements
        self.movement1 = StockMovement(
            product_id=self.product1.id,
            type='inflow',
            amount=10,
            previous_stock=5,
            new_stock=15,
            description='Initial stock'
        )
        
        self.movement2 = StockMovement(
            product_id=self.product2.id,
            type='outflow',
            amount=7,
            previous_stock=10,
            new_stock=3,
            description='Sales'
        )
        
        db.session.add_all([self.movement1, self.movement2])
        db.session.commit()


class TestModels(BaseTestCase):
    """Test database models"""
    
    def test_category_model(self):
        """Test Category model"""
        category = self.category1
        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(str(category), '<Category Electronics>')
        self.assertTrue(len(category.products) > 0)
    
    def test_product_model(self):
        """Test Product model"""
        product = self.product1
        self.assertEqual(product.name, 'Laptop')
        self.assertEqual(product.barcode, '123456789')
        self.assertEqual(product.price, 999.99)
        self.assertEqual(str(product), '<Product Laptop>')
    
    def test_critical_stock_property(self):
        """Test critical stock property"""
        # Normal stock
        self.assertFalse(self.product1.critical_stock)  # stock: 15, min: 5
        
        # Critical stock
        self.assertTrue(self.product2.critical_stock)   # stock: 3, min: 10
    
    def test_stock_movement_model(self):
        """Test StockMovement model"""
        movement = self.movement1
        self.assertEqual(movement.type, 'inflow')
        self.assertEqual(movement.amount, 10)
        self.assertEqual(str(movement), '<StokMovement inflow - 10>')


class TestRoutes(BaseTestCase):
    """Test Flask routes"""
    
    def test_dashboard_route(self):
        """Test dashboard route"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_product_list_route(self):
        """Test product list route"""
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Products', response.data)
        self.assertIn(b'Laptop', response.data)
    
    def test_product_add_route(self):
        """Test product add route"""
        response = self.app.get('/product/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Product', response.data)
    
    def test_category_list_route(self):
        """Test category list route"""
        response = self.app.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Categories', response.data)
        self.assertIn(b'Electronics', response.data)
    
    def test_analytics_route(self):
        """Test analytics route"""
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analytics Dashboard', response.data)
    
    def test_reports_route(self):
        """Test reports route"""
        response = self.app.get('/reports')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reports', response.data)
    
    def test_404_route(self):
        """Test 404 error"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


class TestFunctionality(BaseTestCase):
    """Test application functionality"""
    
    def test_add_product(self):
        """Test adding a new product"""
        form_data = {
            'name': 'New Product',
            'barcode': '999888777',
            'price': 99.99,
            'stock': 50,
            'min_stock': 10,
            'category_id': self.category1.id
        }
        
        response = self.app.post('/product/add', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify product was created
        new_product = Product.query.filter_by(name='New Product').first()
        self.assertIsNotNone(new_product)
        self.assertEqual(new_product.barcode, '999888777')
    
    def test_edit_product(self):
        """Test editing a product"""
        form_data = {
            'name': 'Updated Laptop',
            'barcode': self.product1.barcode,
            'price': 1199.99,
            'min_stock': 8,
            'category_id': self.category1.id
        }
        
        response = self.app.post(f'/product/edit/{self.product1.id}', 
                               data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify product was updated
        updated_product = Product.query.get(self.product1.id)
        self.assertEqual(updated_product.name, 'Updated Laptop')
        self.assertEqual(updated_product.price, 1199.99)
    
    def test_add_category(self):
        """Test adding a new category"""
        form_data = {
            'name': 'New Category',
            'description': 'This is a new category'
        }
        
        response = self.app.post('/category/add', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify category was created
        new_category = Category.query.filter_by(name='New Category').first()
        self.assertIsNotNone(new_category)
    
    def test_stock_movement_inflow(self):
        """Test stock inflow"""
        original_stock = self.product1.stock
        
        form_data = {
            'product_id': self.product1.id,
            'type': 'inflow',
            'amount': 25,
            'description': 'New stock arrival'
        }
        
        response = self.app.post('/stock-movement', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify stock was updated
        updated_product = Product.query.get(self.product1.id)
        self.assertEqual(updated_product.stock, original_stock + 25)
    
    def test_stock_movement_outflow(self):
        """Test stock outflow"""
        original_stock = self.product1.stock
        
        form_data = {
            'product_id': self.product1.id,
            'type': 'outflow',
            'amount': 5,
            'description': 'Sales'
        }
        
        response = self.app.post('/stock-movement', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify stock was updated
        updated_product = Product.query.get(self.product1.id)
        self.assertEqual(updated_product.stock, original_stock - 5)
    
    def test_insufficient_stock_outflow(self):
        """Test outflow with insufficient stock"""
        form_data = {
            'product_id': self.product2.id,  # T-Shirt with stock 3
            'type': 'outflow',
            'amount': 10,  # More than available
            'description': 'Attempted sale'
        }
        
        response = self.app.post('/stock-movement', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Not enough stock', response.data)


class TestExports(BaseTestCase):
    """Test export functionality"""
    
    def test_product_excel_export(self):
        """Test product Excel export"""
        response = self.app.get('/products/export/excel')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    def test_dashboard_pdf_export(self):
        """Test dashboard PDF export"""
        response = self.app.get('/dashboard/export/pdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')
    
    def test_reports_pdf_export(self):
        """Test reports PDF export"""
        response = self.app.get('/reports/export/pdf?start_date=2023-01-01&end_date=2023-12-31')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("FLASK STOCK TRACKING SYSTEM - TEST SUITE")
    print("=" * 70)
    print(f"Starting tests at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestModels,
        TestRoutes,
        TestFunctionality,
        TestExports
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0]}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('\n')[-2]}")
    
    print()
    print("Test completed at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)