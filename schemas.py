from pydantic import BaseModel


class ProductCategoryBase(BaseModel):
    name: str


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int

    class Config:
        orm_model = True
