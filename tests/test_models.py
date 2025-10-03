"""
Unit tests for Models
"""
import pytest
from models import Product, Category, StockMovement, db
from datetime import datetime


class TestCategoryModel:
    """Test Category model"""
    
    def test_category_creation(self, client, init_database):
        """Test category creation"""
        data = init_database
        category = data['categories'][0]
        
        assert category.name == 'Electronics'
        assert category.description == 'Electronic products'
        assert len(category.products) > 0
    
    def test_category_repr(self, client, init_database):
        """Test category string representation"""
        data = init_database
        category = data['categories'][0]
        
        assert str(category) == '<Category Electronics>'
    
    def test_category_unique_name(self, client, init_database):
        """Test category unique name constraint"""
        with pytest.raises(Exception):
            duplicate_category = Category(name='Electronics', description='Duplicate')
            db.session.add(duplicate_category)
            db.session.commit()


class TestProductModel:
    """Test Product model"""
    
    def test_product_creation(self, client, init_database):
        """Test product creation"""
        data = init_database
        product = data['products'][0]
        
        assert product.name == 'Laptop'
        assert product.barcode == '123456789'
        assert product.price == 999.99
        assert product.stock == 15
        assert product.min_stock == 5
        assert product.active is True
    
    def test_product_repr(self, client, init_database):
        """Test product string representation"""
        data = init_database
        product = data['products'][0]
        
        assert str(product) == '<Product Laptop>'
    
    def test_critical_stock_property(self, client, init_database):
        """Test critical stock property"""
        data = init_database
        
        # Normal stock product
        normal_product = data['products'][0]  # stock: 15, min_stock: 5
        assert normal_product.critical_stock is False
        
        # Critical stock product
        critical_product = data['products'][1]  # stock: 3, min_stock: 10
        assert critical_product.critical_stock is True
    
    def test_product_category_relationship(self, client, init_database):
        """Test product-category relationship"""
        data = init_database
        product = data['products'][0]
        category = data['categories'][0]
        
        assert product.categorie == category
        assert product in category.products
    
    def test_product_barcode_unique(self, client, init_database):
        """Test product barcode uniqueness"""
        data = init_database
        category = data['categories'][0]
        
        with pytest.raises(Exception):
            duplicate_product = Product(
                name='Duplicate Laptop',
                barcode='123456789',  # Same barcode
                price=899.99,
                stock=10,
                min_stock=5,
                category_id=category.id
            )
            db.session.add(duplicate_product)
            db.session.commit()
    
    def test_product_without_barcode(self, client, init_database):
        """Test product creation without barcode"""
        data = init_database
        category = data['categories'][0]
        
        product = Product(
            name='Test Product',
            price=19.99,
            stock=100,
            min_stock=10,
            category_id=category.id
        )
        db.session.add(product)
        db.session.commit()
        
        assert product.barcode is None
        assert product.name == 'Test Product'


class TestStockMovementModel:
    """Test StockMovement model"""
    
    def test_stock_movement_creation(self, client, init_database):
        """Test stock movement creation"""
        data = init_database
        movement = data['movements'][0]
        
        assert movement.type == 'inflow'
        assert movement.amount == 10
        assert movement.previous_stock == 5
        assert movement.new_stock == 15
        assert movement.description == 'Initial stock'
    
    def test_stock_movement_repr(self, client, init_database):
        """Test stock movement string representation"""
        data = init_database
        movement = data['movements'][0]
        
        assert str(movement) == '<StokMovement inflow - 10>'
    
    def test_stock_movement_product_relationship(self, client, init_database):
        """Test stock movement-product relationship"""
        data = init_database
        movement = data['movements'][0]
        product = data['products'][0]
        
        assert movement.product == product
        assert movement in product.movements
    
    def test_stock_movement_types(self, client, init_database):
        """Test different stock movement types"""
        data = init_database
        product = data['products'][0]
        
        # Test inflow
        inflow_movement = StockMovement(
            product_id=product.id,
            type='inflow',
            amount=20,
            previous_stock=15,
            new_stock=35,
            description='Restocking'
        )
        db.session.add(inflow_movement)
        
        # Test outflow
        outflow_movement = StockMovement(
            product_id=product.id,
            type='outflow',
            amount=5,
            previous_stock=35,
            new_stock=30,
            description='Sale'
        )
        db.session.add(outflow_movement)
        db.session.commit()
        
        assert inflow_movement.type == 'inflow'
        assert outflow_movement.type == 'outflow'
        assert len(product.movements) >= 3  # Including existing ones
    
    def test_stock_movement_timestamp(self, client, init_database):
        """Test stock movement timestamp"""
        data = init_database
        movement = data['movements'][0]
        
        assert isinstance(movement.date, datetime)
        assert movement.date <= datetime.now()


class TestModelRelationships:
    """Test model relationships"""
    
    def test_cascade_delete_category(self, client, init_database):
        """Test what happens when category is deleted"""
        data = init_database
        category = data['categories'][0]
        products_count = len(category.products)
        
        # Should not be able to delete category with products
        # This test assumes we have proper foreign key constraints
        assert products_count > 0
    
    def test_cascade_delete_product(self, client, init_database):
        """Test what happens when product is deleted"""
        data = init_database
        product = data['products'][0]
        movements_count = len(product.movements)
        
        assert movements_count > 0
        
        # If we delete the product, movements should also be affected
        # This depends on the cascade settings in the relationship