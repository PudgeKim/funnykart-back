import uuid
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


from src.database import engine
from backports.zoneinfo import ZoneInfo
from datetime import datetime

from src.queries import losers, recent_races
from src import models, schemas
from src.utils import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(losers.router, prefix="/races", tags=["losers"])
app.include_router(recent_races.router, prefix="/races", tags=["recent"])


@app.post("/races")
def create_races(races: List[schemas.RaceBase], db: Session = Depends(get_db)):
    group_uuid = str(uuid.uuid4())

    for race_data in races:
        created_at = race_data.created_at or datetime.now(ZoneInfo("Asia/Seoul"))

        race = models.Race(
            group_uuid=group_uuid,
            track_name=race_data.track_name,
            created_at=created_at
        )
        db.add(race)
        db.flush()

        for result in race_data.results:
            db.add(models.RaceResult(
                race_id=race.id,
                rank=result.rank,
                character_name=result.character_name,
                finish_time=result.finish_time
            ))

    db.commit()
    return {"status": "success"}