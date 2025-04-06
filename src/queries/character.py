from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from src import models
from src.utils import get_db

router = APIRouter()


@router.get("/loser-history")
def get_all_loser_history(character_name: str = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.Race.group_uuid,
            models.RaceResult.character_name,
            func.sum(models.RaceResult.rank).label("total_rank"),
            func.min(models.Race.created_at).label("created_at")
        )
            .join(models.RaceResult, models.Race.id == models.RaceResult.race_id)
            .group_by(models.Race.group_uuid, models.RaceResult.character_name)
            .all()
    )

    losers = {}
    for row in rows:
        group = row.group_uuid
        current = losers.get(group)
        if not current or row.total_rank > current.total_rank:
            losers[group] = row

    filtered = [
        {
            "group_uuid": row.group_uuid,
            "character_name": row.character_name,
            "total_rank": row.total_rank,
            "created_at": row.created_at
        }
        for row in losers.values()
        if row.character_name == character_name
    ]

    filtered.sort(key=lambda r: r["created_at"], reverse=True)

    return filtered
