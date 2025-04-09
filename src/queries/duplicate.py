from sqlalchemy.orm import Session

from src import models


def is_duplicate_race(db: Session, group_hash: str) -> bool:
    return db.query(models.Race).filter(models.Race.group_hash == group_hash).first() is not None
