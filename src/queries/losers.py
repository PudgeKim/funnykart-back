from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from src import models
from src.utils import get_db, get_today_range

router = APIRouter()


@router.get("/today-losers")
def get_today_losers(db: Session = Depends(get_db)):
    today_start, tomorrow_start = get_today_range()

    subquery = (
        db.query(
            models.Race.group_uuid,
            models.RaceResult.character_name,
            func.sum(models.RaceResult.rank).label("total_rank")
        )
            .join(models.RaceResult, models.Race.id == models.RaceResult.race_id)
            .filter(models.Race.created_at >= today_start)
            .filter(models.Race.created_at < tomorrow_start)
            .group_by(models.Race.group_uuid, models.RaceResult.character_name)
            .subquery()
    )

    rows = db.query(
        subquery.c.group_uuid,
        subquery.c.character_name,
        subquery.c.total_rank
    ).all()

    # rows example
    # row: ('grp-1', 'Mario', 5)
    # row: ('grp-1', 'Luigi', 3)
    # row: ('grp-2', 'Peach', 1)
    # row: ('grp-2', 'Yoshi', 4)

    # key = group_uuid, value = row
    losers = {}
    for row in rows:
        group = row.group_uuid
        current = losers.get(group)
        if not current or row.total_rank > current.total_rank:
            losers[group] = row

    return [
        {
            "group_uuid": row.group_uuid,
            "character_name": row.character_name,
            "total_rank": row.total_rank
        }
        for row in losers.values()
    ]