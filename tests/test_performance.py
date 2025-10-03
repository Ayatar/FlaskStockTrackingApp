"""
Performance and Load Tests
"""
import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from models import Product, Category, StockMovement, db


class TestPerformance:
    """Test application performance"""
    
    def test_dashboard_load_time(self, client, init_database):
        """Test dashboard loads within acceptable time"""
        start_time = time.time()
        response = client.get('/')
        end_time = time.time()
        
        load_time = end_time - start_time
        
        assert response.status_code == 200
        assert load_time < 2.0  # Should load within 2 seconds
    
    def test_product_list_load_time(self, client, init_database):
        """Test product list loads within acceptable time"""
        start_time = time.time()
        response = client.get('/products')
        end_time = time.time()
        
        load_time = end_time - start_time
        
        assert response.status_code == 200
        assert load_time < 2.0  # Should load within 2 seconds
    
    def test_database_query_performance(self, client, init_database):
        """Test database query performance"""
        # Create more test data
        data = init_database
        category = data['categories'][0]
        
        # Add 100 products for testing
        products = []
        for i in range(100):
            product = Product(
                name=f'Test Product {i}',
                barcode=f'TEST{i:06d}',
                price=19.99 + i,
                stock=100 + i,
                min_stock=10,
                category_id=category.id
            )
            products.append(product)
        
        db.session.add_all(products)
        db.session.commit()
        
        # Test query performance
        start_time = time.time()
        all_products = Product.query.all()
        end_time = time.time()
        
        query_time = end_time - start_time
        
        assert len(all_products) >= 100
        assert query_time < 1.0  # Should query within 1 second
    
    def test_concurrent_requests(self, client, init_database):
        """Test handling concurrent requests"""
        def make_request():
            response = client.get('/')
            return response.status_code
        
        # Make 10 concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # All requests should succeed
        assert all(status == 200 for status in results)
    
    def test_large_data_export(self, client, init_database):
        """Test exporting large amounts of data"""
        data = init_database
        category = data['categories'][0]
        
        # Create more products for testing
        products = []
        for i in range(500):
            product = Product(
                name=f'Export Test Product {i}',
                barcode=f'EXP{i:06d}',
                price=9.99 + (i % 50),
                stock=50 + (i % 100),
                min_stock=5,
                category_id=category.id
            )
            products.append(product)
        
        db.session.add_all(products)
        db.session.commit()
        
        # Test Excel export performance
        start_time = time.time()
        response = client.get('/products/export/excel')
        end_time = time.time()
        
        export_time = end_time - start_time
        
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert export_time < 10.0  # Should export within 10 seconds


class TestDatabaseIntegrity:
    """Test database integrity and constraints"""
    
    def test_foreign_key_constraints(self, client, init_database):
        """Test foreign key constraints"""
        # Try to create product with non-existent category
        with pytest.raises(Exception):
            product = Product(
                name='Invalid Product',
                price=19.99,
                stock=10,
                min_stock=5,
                category_id=999  # Non-existent category
            )
            db.session.add(product)
            db.session.commit()
    
    def test_unique_constraints(self, client, init_database):
        """Test unique constraints"""
        data = init_database
        category = data['categories'][0]
        
        # Try to create product with duplicate barcode
        with pytest.raises(Exception):
            product = Product(
                name='Duplicate Barcode Product',
                barcode='123456789',  # Same as existing product
                price=19.99,
                stock=10,
                min_stock=5,
                category_id=category.id
            )
            db.session.add(product)
            db.session.commit()
    
    def test_data_consistency_after_stock_movements(self, client, init_database):
        """Test data consistency after multiple stock movements"""
        data = init_database
        product = data['products'][0]
        original_stock = product.stock
        
        # Perform multiple stock movements
        movements_data = [
            ('inflow', 20, 'Restock 1'),
            ('outflow', 5, 'Sale 1'),
            ('inflow', 10, 'Restock 2'),
            ('outflow', 15, 'Sale 2'),
        ]
        
        expected_stock = original_stock
        for movement_type, amount, description in movements_data:
            if movement_type == 'inflow':
                expected_stock += amount
            else:
                expected_stock -= amount
            
            movement = StockMovement(
                product_id=product.id,
                type=movement_type,
                amount=amount,
                previous_stock=product.stock,
                new_stock=product.stock + (amount if movement_type == 'inflow' else -amount),
                description=description
            )
            
            # Update product stock
            if movement_type == 'inflow':
                product.stock += amount
            else:
                product.stock -= amount
            
            db.session.add(movement)
        
        db.session.commit()
        
        # Verify final stock matches expected
        final_product = Product.query.get(product.id)
        assert final_product.stock == expected_stock
        
        # Verify all movements were recorded
        all_movements = StockMovement.query.filter_by(product_id=product.id).all()
        assert len(all_movements) >= len(movements_data)


class TestSecurityAndValidation:
    """Test security and input validation"""
    
    def test_sql_injection_protection(self, client, init_database):
        """Test protection against SQL injection"""
        # Try SQL injection in search parameter
        malicious_input = "'; DROP TABLE products; --"
        response = client.get(f'/products?search={malicious_input}')
        
        # Should not cause server error and products table should still exist
        assert response.status_code == 200
        
        # Verify products table still exists by querying it
        products = Product.query.all()
        assert isinstance(products, list)
    
    def test_xss_protection(self, client, init_database):
        """Test protection against XSS attacks"""
        data = init_database
        category = data['categories'][0]
        
        # Try to create product with XSS payload in name
        malicious_name = "<script>alert('XSS')</script>"
        
        form_data = {
            'name': malicious_name,
            'price': 19.99,
            'stock': 10,
            'min_stock': 5,
            'category_id': category.id
        }
        
        response = client.post('/product/add', data=form_data, follow_redirects=True)
        
        # Should not execute script - content should be escaped
        assert response.status_code == 200
        assert b'<script>' not in response.data  # Should be escaped
    
    def test_input_length_limits(self, client, init_database):
        """Test input length limits"""
        data = init_database
        category = data['categories'][0]
        
        # Try extremely long product name
        very_long_name = 'A' * 1000
        
        form_data = {
            'name': very_long_name,
            'price': 19.99,
            'stock': 10,
            'min_stock': 5,
            'category_id': category.id
        }
        
        response = client.post('/product/add', data=form_data)
        
        # Should reject due to length validation
        assert response.status_code == 200
        assert b'Field must be between' in response.data or b'too long' in response.data.lower()
    
    def test_negative_values_protection(self, client, init_database):
        """Test protection against negative values where inappropriate"""
        data = init_database
        category = data['categories'][0]
        
        form_data = {
            'name': 'Test Product',
            'price': -10.0,  # Negative price
            'stock': -5,     # Negative stock
            'min_stock': -1, # Negative min_stock
            'category_id': category.id
        }
        
        response = client.post('/product/add', data=form_data)
        
        # Should reject negative values
        assert response.status_code == 200
        assert b'must be at least 0' in response.data or b'error' in response.data.lower()


class TestDataIntegrity:
    """Test data integrity and business logic"""
    
    def test_critical_stock_calculation(self, client, init_database):
        """Test critical stock property calculation"""
        data = init_database
        category = data['categories'][0]
        
        # Create product with stock equal to min_stock (critical)
        critical_product = Product(
            name='Critical Stock Product',
            price=19.99,
            stock=5,
            min_stock=5,
            category_id=category.id
        )
        db.session.add(critical_product)
        db.session.commit()
        
        assert critical_product.critical_stock is True
        
        # Create product with stock above min_stock (normal)
        normal_product = Product(
            name='Normal Stock Product',
            price=19.99,
            stock=20,
            min_stock=5,
            category_id=category.id
        )
        db.session.add(normal_product)
        db.session.commit()
        
        assert normal_product.critical_stock is False
    
    def test_stock_movement_calculations(self, client, init_database):
        """Test stock movement calculations are correct"""
        data = init_database
        product = data['products'][0]
        initial_stock = product.stock
        
        # Test inflow
        inflow_amount = 25
        movement = StockMovement(
            product_id=product.id,
            type='inflow',
            amount=inflow_amount,
            previous_stock=initial_stock,
            new_stock=initial_stock + inflow_amount
        )
        
        product.stock += inflow_amount
        db.session.add(movement)
        db.session.commit()
        
        # Verify calculations
        assert movement.new_stock == movement.previous_stock + movement.amount
        assert product.stock == initial_stock + inflow_amount
        
        # Test outflow
        current_stock = product.stock
        outflow_amount = 10
        
        movement2 = StockMovement(
            product_id=product.id,
            type='outflow',
            amount=outflow_amount,
            previous_stock=current_stock,
            new_stock=current_stock - outflow_amount
        )
        
        product.stock -= outflow_amount
        db.session.add(movement2)
        db.session.commit()
        
        # Verify calculations
        assert movement2.new_stock == movement2.previous_stock - movement2.amount
        assert product.stock == current_stock - outflow_amount