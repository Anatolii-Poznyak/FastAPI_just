from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class DBProductCategory(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    products = relationship("DBProduct",
                            back_populates="product_category",
                            cascade="all, delete-orphan")


class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(511), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    product_category_id = Column(Integer, ForeignKey("categories.id"))

    product_category = relationship(DBProductCategory)
