from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

import crud
import schemas
from db.engine import async_session
from security import (
    create_access_token,
    oauth_2_scheme,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user,
    authenticate_user
)

app = FastAPI()


async def get_db() -> Session:
    db = async_session()

    try:
        yield db
    finally:
        await db.close()


@app.get("/just/product-categories/", response_model=list[schemas.ProductCategory])
async def read_categories(
   db: Session = Depends(get_db),
   limit: int = 10,
   name: str | None = None
):
    return await crud.get_product_category_list(db=db, limit=limit, name=name)


@app.get("/just/product-categories/{product_category_id}/", response_model=schemas.ProductCategory)
async def read_single_category(
        product_category_id: int,
        db: Session = Depends(get_db)
):
    return await crud.get_product_category(db=db, product_category_id=product_category_id)
#TODO i can make if product_cat is none: raise HTTPException404 "Product not found". where i need to make this validation?


@app.post("/just/product-categories/", response_model=schemas.ProductCategory)
async def create_category(
        product_category: schemas.ProductCategoryCreate,
        db: Session = Depends(get_db)
):
    return await crud.create_product_category(db=db, product_category=product_category)


@app.delete("/just/product-categories/{product_category_id}/")
async def delete_single_category(
        product_category_id: int,
        db: Session = Depends(get_db)
):
    return await crud.delete_product_category(db=db, product_category_id=product_category_id)


@app.put("/just/product-categories/{product_category_id}/", response_model=schemas.ProductCategory)
async def update_category(
        product_category: schemas.ProductCategoryUpdate,
        product_category_id: int,
        db: Session = Depends(get_db)
):
    db_product_category = await crud.update_product_category(
        product_category=product_category,
        product_category_id=product_category_id,
        db=db
    )
    return db_product_category


@app.get("/just/products/", response_model=list[schemas.Product])
async def read_products(
        db: Session = Depends(get_db),
        limit: int = 10,
        name: str = None,
        product_category_id: int = None
):
    return await crud.get_product_list(
        db=db,
        limit=limit,
        name=name,
        product_category_id=product_category_id
    )


@app.get("/just/products/{product_id}/", response_model=schemas.Product)
def read_single_product(
        product_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_product(db=db, product_id=product_id)


@app.post("/just/products/", response_model=schemas.Product)
def create_product(
        product: schemas.ProductCreate,
        db: Session = Depends(get_db)
):
    return crud.create_product(db=db, product=product)


@app.delete("/just/products/{product_id)/")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(product_id=product_id, db=db)


@app.put("/just/products/{product_id}/", response_model=schemas.ProductUpdate)
def update_product(
        product_id: int,
        product: schemas.ProductUpdate,
        db: Session = Depends(get_db)
):
    return crud.update_product(product_id=product_id, product=product, db=db)


@app.patch("/just/products/{product_id)/", response_model=schemas.ProductPartialUpdate)
def partial_update_product(
        product_id: int,
        product: schemas.ProductPartialUpdate,
        db: Session = Depends(get_db)
):
    return crud.partial_update_product(product_id=product_id, product=product, db=db)


@app.post("/token/", response_model=schemas.Token)
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=user.username,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token-type": "bearer"}


@app.post("/sign-up/", response_model=schemas.User)
async def create_user(
        user: schemas.User,
        db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=user)


@app.get("/users/me/", response_model=schemas.User)
def read_me(
        token=Depends(oauth_2_scheme),
        db: Session = Depends(get_db)
):
    user = get_current_user(db=db, token=token)
    return user
