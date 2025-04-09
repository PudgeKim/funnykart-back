from fastapi import Depends, APIRouter
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from src import models
from src.utils import get_db

router = APIRouter()


@router.get("/all")
def get_all_tracks_count(db: Session = Depends(get_db)):
    results = db.query(
        models.Race.track_name, func.count(models.Race.track_name).label('count')
    ).group_by(models.Race.track_name).order_by(desc('count')).limit(20).all()

    track_counts = [{"track_name": name, "count": count} for name, count in results]
    return track_counts
