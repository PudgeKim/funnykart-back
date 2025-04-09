import hashlib
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


from src.database import engine
from zoneinfo import ZoneInfo
from datetime import datetime

from src.queries import losers, recent_races, character
from src import models, schemas
from src.queries.duplicate import is_duplicate_race
from src.utils import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(losers.router, prefix="/races", tags=["losers"])
app.include_router(recent_races.router, prefix="/races", tags=["recent"])
app.include_router(character.router, prefix="/races", tags=["character"])


@app.post("/races")
def create_races(races: List[schemas.RaceBase], db: Session = Depends(get_db)):
    created_at = datetime.now(ZoneInfo("Asia/Seoul"))

    # 첫번째 경기의 정보들로 해시 구성 (중복 데이터 방지에 사용하기 위해)
    first_race = races[0]
    combined_str = ""
    combined_str += first_race.track_name

    for result in first_race.results:
        combined_str += str(result.rank)
        combined_str += result.character_name
        combined_str += result.finish_time

    group_hash = hashlib.sha256(combined_str.encode("utf-8")).hexdigest()
    if is_duplicate_race(db, group_hash):
        raise HTTPException(
            status_code=400,
            detail=f"group_uuid: {group_hash} already exists."
        )

    # DB에 저장
    for race_data in races:
        race = models.Race(
            group_uuid=group_hash,
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
                finish_time=result.finish_time,
            ))

    db.commit()
    return {"status": "success"}