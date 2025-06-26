from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class Buddy(BaseModel):
    buddy_id: str
    last_interaction_days: int
    messages_sent: int
    karma_change_7d: int
    quizzes_attempted: int


class SocialMetrics(BaseModel):
    helpful_answers: int
    profile_completeness: int
    karma_growth: int
    tags_followed: List[str]


class History(BaseModel):
    last_compliment_generated: Optional[date]
    last_buddy_nudge: Optional[date]


class UserData(BaseModel):
    user_id: str
    buddies: List[Buddy]
    social_metrics: SocialMetrics
    history: History
