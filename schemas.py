from datetime import date

from pydantic import BaseModel


class ProductCategoryBase(BaseModel):
    name: str


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(ProductCategoryBase):
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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class User(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True
