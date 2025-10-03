"""
Test configuration file for Flask Stock Tracking System
"""
import os
import tempfile
import pytest
from app import app, db
from models import Product, Category, StockMovement


class TestConfig:
    """Test configuration class"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    WTF_CSRF_ENABLED = False


@pytest.fixture
def client():
    """Create test client"""
    app.config.from_object(TestConfig)
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def init_database():
    """Initialize database with test data"""
    with app.app_context():
        # Create test categories
        category1 = Category(name='Electronics', description='Electronic products')
        category2 = Category(name='Clothing', description='Clothing items')
        category3 = Category(name='Books', description='Books and literature')
        
        db.session.add_all([category1, category2, category3])
        db.session.commit()
        
        # Create test products
        product1 = Product(
            name='Laptop',
            barcode='123456789',
            price=999.99,
            stock=15,
            min_stock=5,
            category_id=category1.id
        )
        
        product2 = Product(
            name='T-Shirt',
            barcode='987654321',
            price=29.99,
            stock=3,  # Critical stock
            min_stock=10,
            category_id=category2.id
        )
        
        product3 = Product(
            name='Python Book',
            price=49.99,
            stock=25,
            min_stock=5,
            category_id=category3.id
        )
        
        db.session.add_all([product1, product2, product3])
        db.session.commit()
        
        # Create test stock movements
        movement1 = StockMovement(
            product_id=product1.id,
            type='inflow',
            amount=10,
            previous_stock=5,
            new_stock=15,
            description='Initial stock'
        )
        
        movement2 = StockMovement(
            product_id=product2.id,
            type='outflow',
            amount=7,
            previous_stock=10,
            new_stock=3,
            description='Sales'
        )
        
        db.session.add_all([movement1, movement2])
        db.session.commit()
        
        return {
            'categories': [category1, category2, category3],
            'products': [product1, product2, product3],
            'movements': [movement1, movement2]
        }


@pytest.fixture
def auth_headers():
    """Authentication headers for API tests"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }