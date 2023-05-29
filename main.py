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
