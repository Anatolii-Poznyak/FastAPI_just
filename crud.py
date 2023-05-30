from sqlalchemy.orm import Session, selectinload
from db import models
import schemas
from security import get_password_hash
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from db import models
import schemas
from security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession


async def get_product_category_list(
    db: AsyncSession,
    limit: int = 10,
    name: str = None
):
    stmt = select(models.DBProductCategory).limit(limit)
    result = await db.execute(stmt)
    queryset = result.scalars().all()

    if name:
        stmt = stmt.filter(models.DBProductCategory.name.ilike(f'%{name}%'))
        result = await db.execute(stmt)
        queryset = result.scalars().all()

    return queryset


#TODO How to get rid of code duplications !
async def get_product_category(
        db: AsyncSession,
        product_category_id: int
):
    stmt = select(models.DBProductCategory).where(models.DBProductCategory.id == product_category_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def delete_product_category(
        db: AsyncSession,
        product_category_id: int
):
    stmt = delete(models.DBProductCategory).where(models.DBProductCategory.id == product_category_id)
    await db.execute(stmt)
    await db.commit()


async def create_product_category(
        db: AsyncSession,
        product_category: schemas.ProductCategoryCreate
):
    db_product_category = models.DBProductCategory(
        name=product_category.name
    )
    db.add(db_product_category)
    await db.commit()
    await db.refresh(db_product_category)

    return db_product_category


async def update_product_category(
        db: AsyncSession,
        product_category_id: int,
        product_category: schemas.ProductCategoryUpdate
):
    stmt = select(models.DBProductCategory).where(models.DBProductCategory.id == product_category_id)
    result = await db.execute(stmt)
    db_product_category = result.scalar_one_or_none()

    if db_product_category:
        db_product_category.name = product_category.name
        db.add(db_product_category)
        await db.commit()
        await db.refresh(db_product_category)

    return db_product_category


async def get_product_list(
    db: AsyncSession,
    limit: int = 10,
    name: str = None,
    product_category_id: int = None
):
    stmt = select(models.DBProduct).options(selectinload(models.DBProduct.product_category)).limit(limit)
    result = await db.execute(stmt)
    queryset = result.scalars().all()

    if name:
        stmt = stmt.filter(models.DBProduct.name.ilike(f'%{name}%'))
        result = await db.execute(stmt)
        queryset = result.scalars().all()

    if product_category_id:
        stmt = stmt.filter(models.DBProduct.product_category_id == product_category_id)
        result = await db.execute(stmt)
        queryset = result.scalars().first()

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


def update_product(db: Session, product: schemas.ProductUpdate, product_id: int):
    db_product = db.query(models.DBProduct).filter(models.DBProduct.id == product_id).first()
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.created_at = product.created_at
#TODO db.add? Am I Sure?
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def partial_update_product(db: Session, product: schemas.ProductPartialUpdate, product_id: int):
    db_product = db.query(models.DBProduct).filter(models.DBProduct.id == product_id).first()
    db_product.name = product.name if product.name else db_product.name
    db_product.description = product.description if product.description else db_product.description
    db_product.price = product.price if product.price else db_product.price
    db_product.created_at = product.created_at if product.created_at else db_product.created_at
    db_product.category_id = product.product_category_id if product.product_category_id else db_product.product_category_id

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_user(db: Session, user: schemas.User):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
