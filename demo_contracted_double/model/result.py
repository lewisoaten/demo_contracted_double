from datetime import datetime
from pydantic import BaseModel, Field


class Result(BaseModel):
    time: datetime = Field(default_factory=datetime.utcnow)
    first: int
    second: int
    result: int