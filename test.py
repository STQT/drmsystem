from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import random

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    transaction_id = Column(Integer)

    user = relationship(User)
    products = relationship('Product', secondary='order_product')


class OrderProduct(Base):
    __tablename__ = 'order_product'
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer)


# Create the engine and session
engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Create mock data for users
users = [
    User(name='John'),
    User(name='Emily'),
    User(name='Michael'),
    User(name='Sophia')
]
session.add_all(users)
session.commit()

# Create mock data for products
products = [
    Product(name='Product 1'),
    Product(name='Product 2'),
    Product(name='Product 3'),
    Product(name='Product 4')
]
session.add_all(products)
session.commit()

# Create mock data for orders
orders = [
    Order(user_id=1, transaction_id=1001),
    Order(user_id=2, transaction_id=1002),
    Order(user_id=3, transaction_id=1003),
    Order(user_id=4, transaction_id=1004)
]
session.add_all(orders)
session.commit()

# Create mock data for order products
order_products = []
for order in orders:
    product_ids = random.sample(range(1, len(products) + 1), random.randint(1, len(products)))
    for product_id in product_ids:
        quantity = random.randint(1, 5)
        order_product = OrderProduct(order_id=order.id, product_id=product_id, quantity=quantity)
        order_products.append(order_product)
session.add_all(order_products)
session.commit()

# Close the session
session.close()
