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

