"""
Fixed Test runner script for Flask Stock Tracking System
"""
import os
import sys
import unittest
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Ensure tests use isolated database
TEST_DB_PATH = os.path.join(project_root, 'test_unit.sqlite')
os.environ['DATABASE_URL'] = f'sqlite:///{TEST_DB_PATH}'

# Import after path setup
from app import app, db
from models import Product, Category, StockMovement

class TestConfig:
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{TEST_DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    WTF_CSRF_ENABLED = False

class BaseTestCase(unittest.TestCase):
    """Base test case with setup and teardown"""
    
    def setUp(self):
        """Set up test environment"""
        # Configure test app
        app.config.from_object(TestConfig)
        
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Ensure clean schema for each test
        db.drop_all()
        # Create tables
        db.create_all()
        
        # Create test data
        self.create_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def create_test_data(self):
        """Create test data"""
        try:
            # Create categories
            self.category1 = Category(name='Test Electronics', description='Electronic products (test)')
            self.category2 = Category(name='Test Clothing', description='Clothing items (test)')
            
            db.session.add_all([self.category1, self.category2])
            db.session.commit()
            
            # Create products
            self.product1 = Product(
                name='Laptop',
                barcode='TEST-LAP-001',
                price=1000.0,
                stock=10,
                min_stock=5,
                category_id=self.category1.id,
            )
            
            self.product2 = Product(
                name='T-Shirt',
                barcode='TEST-TSH-001',
                price=20.0,
                stock=3,  # Critical stock
                min_stock=10,
                category_id=self.category2.id,
            )
            
            db.session.add_all([self.product1, self.product2])
            db.session.commit()
            
            # Create stock movements
            self.movement1 = StockMovement(
                product_id=self.product1.id,
                type='inflow',
                amount=5,
                previous_stock=5,
                new_stock=10,
                description='Initial stock'
            )
            
            db.session.add(self.movement1)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating test data: {e}")

class TestModels(BaseTestCase):
    """Test database models"""
    
    def test_category_model(self):
        """Test Category model"""
        category = Category.query.filter_by(name='Test Electronics').first()
        self.assertIsNotNone(category)
        self.assertEqual(category.name, 'Test Electronics')
        self.assertEqual(category.description, 'Electronic products (test)')
    
    def test_product_model(self):
        """Test Product model"""
        product = Product.query.filter_by(barcode='TEST-LAP-001').first()
        self.assertIsNotNone(product)
        self.assertEqual(product.name, 'Laptop')
        self.assertEqual(product.price, 1000.0)
        self.assertEqual(product.stock, 10)
    
    def test_stock_movement_model(self):
        """Test StockMovement model"""
        movement = StockMovement.query.filter_by(type='inflow').first()
        self.assertIsNotNone(movement)
        self.assertEqual(movement.amount, 5)
        self.assertIsNotNone(movement.product_id)

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
    
    def test_category_list_route(self):
        """Test category list route"""
        response = self.app.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Categories', response.data)

class TestBasicFunctionality(BaseTestCase):
    """Test basic CRUD functionality"""
    
    def test_category_creation(self):
        """Test category creation"""
        category_count = Category.query.count()
        new_category = Category(name='Food', description='Food items')
        db.session.add(new_category)
        db.session.commit()
        
        self.assertEqual(Category.query.count(), category_count + 1)
        self.assertIsNotNone(Category.query.filter_by(name='Food').first())
    
    def test_product_creation(self):
        """Test product creation"""
        product_count = Product.query.count()
        
        new_product = Product(
            name='Mouse',
            barcode='TEST-MOU-001',
            price=25.0,
            stock=15,
            min_stock=5,
            category_id=self.category1.id,
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        self.assertEqual(Product.query.count(), product_count + 1)
    
    def test_stock_movement_creation(self):
        """Test stock movement creation"""
        movement_count = StockMovement.query.count()
        
        new_movement = StockMovement(
            product_id=self.product1.id,
            type='outflow',
            amount=2,
            previous_stock=self.product1.stock,
            new_stock=self.product1.stock - 2,
            description='Test outflow'
        )
        
        db.session.add(new_movement)
        db.session.commit()
        
        self.assertEqual(StockMovement.query.count(), movement_count + 1)

def run_basic_tests():
    """Run a basic subset of tests"""
    print("Running basic tests for Flask Stock Tracking System")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    suite.addTests(loader.loadTestsFromTestCase(TestRoutes))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicFunctionality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2] if '\n' in traceback else traceback
            print(f"- {test}: {error_msg}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\nSuccess rate: {success_rate:.1f}%")
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_basic_tests()
    sys.exit(0 if success else 1)