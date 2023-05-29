from fastapi import FastAPI
from sqlalchemy.orm import Session

from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

