from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

# Max questions per session × max points per question.
# Practice:    10 questions × 1 point   = 10
# Competition: 20 questions × 1000 pts  = 20000 (use 20000 as a safe ceiling)
_SCORE_LIMITS: dict[str, int] = {
    "practice": 10,
    "competition": 20_000,
}


class ScoreCreate(BaseModel):
    subject: str = Field(min_length=2, max_length=50)
    score: int = Field(ge=0)
    mode: Literal["practice", "competition"]

    @model_validator(mode="after")
    def check_score_ceiling(self) -> "ScoreCreate":
        ceiling = _SCORE_LIMITS.get(self.mode)
        if ceiling is not None and self.score > ceiling:
            raise ValueError(
                f"Score {self.score} exceeds the maximum allowed for '{self.mode}' mode ({ceiling})."
            )
        return self


class ScoreResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    score: int
    mode: str
    completed_at: datetime


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    total_score: int
    completed_runs: int


class LeaderboardResponse(BaseModel):
    mode: str | None
    limit: int
    entries: list[LeaderboardEntry]
