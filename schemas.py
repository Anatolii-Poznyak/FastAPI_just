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
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    created_at: date
    product_category_id: int


class ProductCreate(ProductBase):
    product_category_id: int


class ProductUpdate(ProductBase):
    pass


class ProductPartialUpdate(BaseModel):
    name: str | None
    description: str | None
    price: int | None
    created_at: date | None
    product_category_id: int | None


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
