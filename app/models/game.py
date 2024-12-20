from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel, Field
from typing import List

# 游戏尝试表模型
class GameAttempt(Base):
    __tablename__ = 'game_attempts'

    attempt_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_name = Column(String(50), nullable=False)
    score = Column(Integer, default=0)
    attempts = Column(Integer, nullable=False)
    result = Column(Enum('win', 'lose'), nullable=False)
    played_at = Column(DateTime, default=func.now())

    # 关系
    user = relationship("User", back_populates="game_attempts")

# 游戏统计表模型
class GameStats(Base):
    __tablename__ = 'game_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_name = Column(String(50), nullable=False)
    total_score = Column(Integer, default=0)
    games_played = Column(Integer, default=0)
    average_score = Column(Float, default=0.00)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    play_count = Column(Integer, default=0)
    min_attempts = Column(Integer, nullable=True)
    max_attempts = Column(Integer, nullable=True)
    last_played = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="game_stats")   
    
class LeaderboardEntry(BaseModel):
    user_id: int = Field(..., alias="用户id")
    username: str = Field(..., alias="用户名")
    average_score: float = Field(..., alias="平均分")
    games_played: int = Field(..., alias="游戏次数")
    rank: int = Field(..., alias="排名")

class LeaderboardResponse(BaseModel):
    leaderboard: List[LeaderboardEntry]
    user_rank: int = Field(..., alias="你的排名")
    user_average_score: float = Field(..., alias="平均成绩")
