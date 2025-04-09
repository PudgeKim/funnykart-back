from sqlalchemy.orm import Session

from src import models


def is_duplicate_race(db: Session, group_uuid: str) -> bool:
    return db.query(models.Race).filter(models.Race.group_uuid == group_uuid).first() is not None
