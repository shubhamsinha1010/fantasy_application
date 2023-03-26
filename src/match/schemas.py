from typing import Optional
from pydantic import BaseModel


class MatchAddSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    team_1:str
    team_2:str
    series_name:str
    has_mega_contest: bool
    is_match_open: bool
    deadline: str


class MatchUpdateSchema(BaseModel):
    is_match_open: Optional[bool]
    deadline: Optional[str]