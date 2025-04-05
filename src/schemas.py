from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ResultBase(BaseModel):
    rank: int
    character_name: str
    finish_time: str


class RaceBase(BaseModel):
    track_name: str
    results: List[ResultBase]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True