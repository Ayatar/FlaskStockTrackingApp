from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    
    # Relation
    products = db.relationship('Product', backref='categorie', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=10)  # Kritik stok seviyesi
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    active = db.Column(db.Boolean, default=True)
    
    # Relation
    movements = db.relationship('StockMovement', backref='product', lazy=True)
    
    # Property decaratoru ile fonkisyonu değişken gibi kullanabiliriz.
    @property
    def critical_stock(self):
        """Are the stocks at a critical level?"""
        return self.stock <= self.min_stock
    
    def __repr__(self):
        return f'<Product {self.name}>'


class StockMovement(db.Model):
    __tablename__ = 'stock_movements'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'inflow' or 'outflow'
    amount = db.Column(db.Integer, nullable=False)
    previous_stock = db.Column(db.Integer)
    new_stock = db.Column(db.Integer)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<StokMovement {self.type} - {self.amount}>'