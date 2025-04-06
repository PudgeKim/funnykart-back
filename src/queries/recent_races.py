from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import models
from src.utils import get_recent_days_range, get_db

router = APIRouter()


@router.get("/recent-races")
def get_recent_races(db: Session = Depends(get_db)):
    start_time, end_time = get_recent_days_range(3)

    recent_races = (
        db.query(models.Race)
            .filter(models.Race.created_at >= start_time)
            .filter(models.Race.created_at <= end_time)
            .order_by(models.Race.created_at.asc())
            .all()
    )

    result = []
    for race in recent_races:
        result.append({
            "group_uuid": race.group_uuid,
            "track_name": race.track_name,
            "created_at": race.created_at,
            "results": [
                {
                    "character_name": r.character_name,
                    "rank": r.rank,
                }
                for r in race.results
            ]
        })

    return result
