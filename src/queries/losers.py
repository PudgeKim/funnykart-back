from fastapi import APIRouter, Depends
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from src import models
from src.utils import get_db, get_today_range, get_recent_days_range

router = APIRouter()


@router.get("/today-losers")
def get_today_losers(db: Session = Depends(get_db)):
    start_time, end_time = get_today_range()

    subquery = (
        db.query(
            models.Race.group_uuid,
            models.RaceResult.character_name,
            func.sum(models.RaceResult.rank).label("total_rank")
        )
            .join(models.RaceResult, models.Race.id == models.RaceResult.race_id)
            .filter(models.Race.created_at >= start_time)
            .filter(models.Race.created_at < end_time)
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


@router.get("/recent-losers")
def get_recent_losers(db: Session = Depends(get_db)):
    start_time, end_time = get_recent_days_range(5)

    subquery = (
        db.query(
            models.Race.group_uuid,
            models.RaceResult.character_name,
            models.Race.created_at,
            func.sum(models.RaceResult.rank).label("total_rank")
        )
            .join(models.RaceResult, models.Race.id == models.RaceResult.race_id)
            .filter(models.Race.created_at >= start_time)
            .filter(models.Race.created_at < end_time)
            .group_by(models.Race.group_uuid, models.RaceResult.character_name)
            .order_by(desc(models.Race.created_at))
            .subquery()
    )

    rows = db.query(
        subquery.c.group_uuid,
        subquery.c.character_name,
        subquery.c.created_at,
        subquery.c.total_rank
    ).all()

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
            "total_rank": row.total_rank,
            "created_at": row.created_at
        }
        for row in losers.values()
    ]
