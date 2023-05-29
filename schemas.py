from datetime import date

from pydantic import BaseModel


class ProductCategoryBase(BaseModel):
    name: str


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int

    class Config:
        orm_model = True


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    created_at: date
    product_category: ProductCategoryBase


class ProductCreate(ProductBase):
    product_category_id: int


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
