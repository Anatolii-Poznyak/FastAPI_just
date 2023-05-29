from sqlalchemy.orm import Session
from db import models
import schemas


def get_product_category_list(
        db: Session,
        limit: int = 10,
        name: str = None
):
    queryset = db.query(models.DBProductCategory).limit(limit).all()
    if name:
        return queryset.filter(models.DBProductCategory.name.icontains(name)).all()
    return queryset


def get_product_category(
        db: Session,
        product_category_id: int
):
    return db.query(models.DBProductCategory).filter(models.DBProductCategory.id == product_category_id).first()


def delete_product_category(
        db: Session,
        product_category_id: int
):

    db.query(models.DBProductCategory).filter(models.DBProductCategory.id == product_category_id).delete()
    db.commit()


def create_product_category(
        db: Session,
        product_category: schemas.ProductCategoryCreate
):
    db_product_category = models.DBProductCategory(
        name=product_category.name
    )
    db.add(db_product_category)
    db.commit()
    db.refresh(db_product_category)


def get_product_list(
        db: Session,
        limit: int = 10,
        name: str = None,
        product_category_id: int = None
):
    queryset = db.query(models.DBProduct).limit(limit).all()
    if name:
        return queryset.filter(models.DBProduct.name.icontains(name)).all()
    if product_category_id:
        return queryset.filter(models.DBProduct.product_category_id == product_category_id).first()

    return queryset


def get_product(db: Session, product_id: int):
    return db.query(models.DBProduct).filter(models.DBProduct.id == product_id).first()


def delete_product(db: Session, product_id: int):
    db.query(models.DBProduct).filter(models.DBProduct.id == product_id).delete()
    db.commit()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.DBProduct(
        name=product.name,
        description=product.description,
        price=product.price,
        created_at=product.created_at,
        product_category_id=product.product_category_id
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
