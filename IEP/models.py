import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func

database = SQLAlchemy()


class User(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(256), nullable=False, unique=True)
    password = database.Column(database.String(256), nullable=False)
    forename = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    role = database.Column(database.String(256), nullable=False)


class ProductCategory(database.Model):
    __tablename__ = "product_categories"

    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    categoryId = database.Column(database.Integer, database.ForeignKey("categories.id"), nullable=False)


class Product(database.Model):
    __tablename__ = "products"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Float, nullable=False)

    categories = database.relationship("Category", secondary=ProductCategory.__table__, back_populates="products")
    order_requests = database.relationship("OrderRequest", backref="product")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Category(database.Model):
    __tablename__ = "categories"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)

    products = database.relationship("Product", secondary=ProductCategory.__table__, back_populates="categories")


class OrderRequest(database.Model):
    __tablename__ = "orderrequests"

    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('products.id'))
    order_id = database.Column(database.Integer, database.ForeignKey('orders.id'))
    requested = database.Column(database.Integer, nullable=False, default=0)
    received = database.Column(database.Integer, default=0)
    product_price = database.Column(database.Float, nullable=False)


class Order(database.Model):
    __tablename__ = "orders"

    id = database.Column(database.Integer, primary_key=True)
    requests = database.relationship("OrderRequest", backref='order')
    user_email = database.Column(database.String(256), nullable=False)
    timestamp = database.Column(DateTime(timezone=False), server_default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
