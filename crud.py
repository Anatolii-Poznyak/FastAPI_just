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
