"""
Integration tests for Flask routes
"""
import pytest
import json
from models import Product, Category, StockMovement, db


class TestDashboardRoutes:
    """Test dashboard related routes"""
    
    def test_dashboard_get(self, client, init_database):
        """Test dashboard page loads successfully"""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'Dashboard' in response.data
        assert b'Total Products' in response.data
        assert b'Total Stock' in response.data
    
    def test_dashboard_pdf_export(self, client, init_database):
        """Test dashboard PDF export"""
        response = client.get('/dashboard/export/pdf')
        
        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert 'dashboard_report_' in response.headers['Content-Disposition']


class TestProductRoutes:
    """Test product related routes"""
    
    def test_product_list_get(self, client, init_database):
        """Test product list page"""
        response = client.get('/products')
        
        assert response.status_code == 200
        assert b'Products' in response.data
        assert b'Laptop' in response.data
        assert b'T-Shirt' in response.data
    
    def test_product_list_with_search(self, client, init_database):
        """Test product list with search parameter"""
        response = client.get('/products?search=Laptop')
        
        assert response.status_code == 200
        assert b'Laptop' in response.data
        assert b'T-Shirt' not in response.data
    
    def test_product_list_with_category_filter(self, client, init_database):
        """Test product list with category filter"""
        data = init_database
        electronics_category = data['categories'][0]
        
        response = client.get(f'/products?category={electronics_category.id}')
        
        assert response.status_code == 200
        assert b'Laptop' in response.data
        assert b'T-Shirt' not in response.data
    
    def test_product_add_get(self, client, init_database):
        """Test product add form page"""
        response = client.get('/product/add')
        
        assert response.status_code == 200
        assert b'Add New Product' in response.data
        assert b'Product Name' in response.data
    
    def test_product_add_post_valid(self, client, init_database):
        """Test adding a new product with valid data"""
        data = init_database
        category = data['categories'][0]
        
        form_data = {
            'name': 'New Product',
            'barcode': '999888777',
            'price': 99.99,
            'stock': 50,
            'min_stock': 10,
            'category_id': category.id
        }
        
        response = client.post('/product/add', data=form_data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'successfully added' in response.data
        
        # Verify product was created
        new_product = Product.query.filter_by(name='New Product').first()
        assert new_product is not None
        assert new_product.barcode == '999888777'
    
    def test_product_add_post_invalid(self, client, init_database):
        """Test adding a product with invalid data"""
        form_data = {
            'name': '',  # Empty name
            'price': -10,  # Negative price
            'stock': 50,
            'min_stock': 10,
            'category_id': 1
        }
        
        response = client.post('/product/add', data=form_data)
        
        assert response.status_code == 200
        assert b'This field is required' in response.data or b'error' in response.data.lower()
    
    def test_product_edit_get(self, client, init_database):
        """Test product edit form page"""
        data = init_database
        product = data['products'][0]
        
        response = client.get(f'/product/edit/{product.id}')
        
        assert response.status_code == 200
        assert b'Edit Product' in response.data
        assert product.name.encode() in response.data
    
    def test_product_edit_post_valid(self, client, init_database):
        """Test editing a product with valid data"""
        data = init_database
        product = data['products'][0]
        category = data['categories'][0]
        
        form_data = {
            'name': 'Updated Laptop',
            'barcode': product.barcode,
            'price': 1199.99,
            'min_stock': 8,
            'category_id': category.id
        }
        
        response = client.post(f'/product/edit/{product.id}', data=form_data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'was updated' in response.data
        
        # Verify product was updated
        updated_product = Product.query.get(product.id)
        assert updated_product.name == 'Updated Laptop'
        assert updated_product.price == 1199.99
    
    def test_product_edit_nonexistent(self, client, init_database):
        """Test editing a non-existent product"""
        response = client.get('/product/edit/999')
        
        assert response.status_code == 404
    
    def test_product_delete_post(self, client, init_database):
        """Test deleting a product"""
        data = init_database
        # Use product without movements for successful deletion
        product = data['products'][2]  # Python Book has no movements
        
        response = client.post(f'/product/delete/{product.id}', follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify product was deleted
        deleted_product = Product.query.get(product.id)
        assert deleted_product is None
    
    def test_product_delete_with_movements(self, client, init_database):
        """Test deleting a product with stock movements"""
        data = init_database
        product = data['products'][0]  # Laptop has movements
        
        response = client.post(f'/product/delete/{product.id}', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Cannot delete product' in response.data
        
        # Verify product was not deleted
        existing_product = Product.query.get(product.id)
        assert existing_product is not None
    
    def test_product_export_excel(self, client, init_database):
        """Test product Excel export"""
        response = client.get('/products/export/excel')
        
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert 'products_' in response.headers['Content-Disposition']


class TestCategoryRoutes:
    """Test category related routes"""
    
    def test_category_list_get(self, client, init_database):
        """Test category list page"""
        response = client.get('/categories')
        
        assert response.status_code == 200
        assert b'Categories' in response.data
        assert b'Electronics' in response.data
        assert b'Clothing' in response.data
    
    def test_category_add_get(self, client, init_database):
        """Test category add form page"""
        response = client.get('/category/add')
        
        assert response.status_code == 200
        assert b'Add New Category' in response.data
        assert b'Category Name' in response.data
    
    def test_category_add_post_valid(self, client, init_database):
        """Test adding a new category with valid data"""
        form_data = {
            'name': 'New Category',
            'description': 'This is a new category'
        }
        
        response = client.post('/category/add', data=form_data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'successfully added' in response.data
        
        # Verify category was created
        new_category = Category.query.filter_by(name='New Category').first()
        assert new_category is not None
        assert new_category.description == 'This is a new category'
    
    def test_category_edit_get(self, client, init_database):
        """Test category edit form page"""
        data = init_database
        category = data['categories'][0]
        
        response = client.get(f'/category/edit/{category.id}')
        
        assert response.status_code == 200
        assert b'Edit Category' in response.data
        assert category.name.encode() in response.data
    
    def test_category_edit_post_valid(self, client, init_database):
        """Test editing a category with valid data"""
        data = init_database
        category = data['categories'][0]
        
        form_data = {
            'name': 'Updated Electronics',
            'description': 'Updated electronic products category'
        }
        
        response = client.post(f'/category/edit/{category.id}', data=form_data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'was updated' in response.data
        
        # Verify category was updated
        updated_category = Category.query.get(category.id)
        assert updated_category.name == 'Updated Electronics'
    
    def test_category_delete_with_products(self, client, init_database):
        """Test deleting a category with products"""
        data = init_database
        category = data['categories'][0]  # Electronics has products
        
        response = client.post(f'/category/delete/{category.id}', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Cannot delete category' in response.data
        
        # Verify category was not deleted
        existing_category = Category.query.get(category.id)
        assert existing_category is not None


class TestStockMovementRoutes:
    """Test stock movement related routes"""
    
    def test_stock_movement_get(self, client, init_database):
        """Test stock movement form page"""
        response = client.get('/stock-movement')
        
        assert response.status_code == 200
        assert b'Stock Movement' in response.data
        assert b'Product' in response.data
        assert b'Process Type' in response.data
    
    def test_stock_movement_post_inflow(self, client, init_database):
        """Test adding stock inflow"""
        data = init_database
        product = data['products'][0]
        original_stock = product.stock
        
        form_data = {
            'product_id': product.id,
            'type': 'inflow',
            'amount': 25,
            'description': 'New stock arrival'
        }
        
        response = client.post('/stock-movement', data=form_data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Stock movement recorded' in response.data
        
        # Verify stock was updated
        updated_product = Product.query.get(product.id)
        assert updated_product.stock == original_stock + 25
        
        # Verify movement was recorded
        movement = StockMovement.query.filter_by(
            product_id=product.id, 
            type='inflow', 
            amount=25
        ).first()
        assert movement is not None
    
    def test_stock_movement_post_outflow(self, client, init_database):
        """Test stock outflow"""
        data = init_database
        product = data['products'][0]  # Laptop with stock 15
        original_stock = product.stock
        
        form_data = {
            'product_id': product.id,
            'type': 'outflow',
            'amount': 5,
            'description': 'Sales'
        }
        
        response = client.post('/stock-movement', data=form_data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Stock movement recorded' in response.data
        
        # Verify stock was updated
        updated_product = Product.query.get(product.id)
        assert updated_product.stock == original_stock - 5
    
    def test_stock_movement_insufficient_stock(self, client, init_database):
        """Test outflow with insufficient stock"""
        data = init_database
        product = data['products'][1]  # T-Shirt with stock 3
        
        form_data = {
            'product_id': product.id,
            'type': 'outflow',
            'amount': 10,  # More than available stock
            'description': 'Attempted sale'
        }
        
        response = client.post('/stock-movement', data=form_data)
        
        assert response.status_code == 200
        assert b'Not enough stock' in response.data
        
        # Verify stock was not changed
        unchanged_product = Product.query.get(product.id)
        assert unchanged_product.stock == 3


class TestAnalyticsRoutes:
    """Test analytics related routes"""
    
    def test_analytics_get(self, client, init_database):
        """Test analytics dashboard page"""
        response = client.get('/analytics')
        
        assert response.status_code == 200
        assert b'Analytics Dashboard' in response.data
        assert b'SUMMARY STATISTICS' in response.data


class TestReportRoutes:
    """Test report related routes"""
    
    def test_reports_get(self, client, init_database):
        """Test reports page"""
        response = client.get('/reports')
        
        assert response.status_code == 200
        assert b'Reports' in response.data
        assert b'Starting Date' in response.data
        assert b'Ending Date' in response.data
    
    def test_reports_generate_post(self, client, init_database):
        """Test generating a report"""
        form_data = {
            'starting_date': '2023-01-01',
            'ending_date': '2023-12-31',
            'category_id': ''
        }
        
        response = client.post('/reports/generate', data=form_data)
        
        assert response.status_code == 200
        assert b'Report Results' in response.data or b'products' in response.data.lower()
    
    def test_reports_export_excel(self, client, init_database):
        """Test report Excel export"""
        response = client.get('/reports/export/excel?start_date=2023-01-01&end_date=2023-12-31')
        
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    def test_reports_export_pdf(self, client, init_database):
        """Test report PDF export"""
        response = client.get('/reports/export/pdf?start_date=2023-01-01&end_date=2023-12-31')
        
        assert response.status_code == 200
        assert response.content_type == 'application/pdf'


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error for non-existent routes"""
        response = client.get('/nonexistent-route')
        assert response.status_code == 404
    
    def test_product_not_found(self, client, init_database):
        """Test 404 for non-existent product"""
        response = client.get('/product/edit/999')
        assert response.status_code == 404
    
    def test_category_not_found(self, client, init_database):
        """Test 404 for non-existent category"""
        response = client.get('/category/edit/999')
        assert response.status_code == 404