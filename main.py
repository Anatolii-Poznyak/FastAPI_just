from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/just/product-categories/", response_model=list[schemas.ProductCategory])
def read_categories(
        db: Session = Depends(get_db),
        limit: int = 10,
        name: str | None = None
):
    return crud.get_product_category_list(db=db, limit=limit, name=name)


@app.get("/just/product-categories/{product_category_id}/", response_model=schemas.ProductCategory)
def read_single_category(
        product_category_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_product_category(db=db, product_category_id=product_category_id)
#TODO i can make if product_cat is none: raise HTTPException404 "Product not found". where i need to make this validation?


@app.post("/just/product-categories/", response_model=schemas.ProductCategory):
def create_product_category(
        product_category = schemas.ProductCategoryCreate,
        db: Session = Depends(get_db)
):
    return crud.create_product_category(db=db, product_category=product_category)



