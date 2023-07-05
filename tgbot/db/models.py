from sqlalchemy.orm import relationship

from datetime import datetime
from distutils.sysconfig import get_makefile_filename
from sqlalchemy import (
    Column, BigInteger,
    String, Integer,
    DateTime, Text, ForeignKey
)

from tgbot.db.base import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


class User(Base):
    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String(50))
    first_name = Column(String(50))
