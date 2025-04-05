from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    group_uuid = Column(String, index=True) # 내기 한번에 총 5판을 했다면 5판은 group_uuid 값이 같음
    track_name = Column(String)
    created_at = Column(DateTime, nullable=False)

    results = relationship("RaceResult", back_populates="race")


class RaceResult(Base):
    __tablename__ = "race_results"

    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.id"))
    rank = Column(Integer)
    character_name = Column(String)
    finish_time = Column(String)

    race = relationship("Race", back_populates="results")