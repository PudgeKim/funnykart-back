from fastapi import Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from src import models
from src.utils import get_db

router = APIRouter()


@router.get("/all")
def get_all_tracks_count(db: Session = Depends(get_db)):
    results = db.query(
        models.Race.track_name, func.count(models.Race.track_name)
    ).group_by(models.Race.track_name).all()

    track_counts = [{"track_name": name, "count": count} for name, count in results]
    return track_counts
