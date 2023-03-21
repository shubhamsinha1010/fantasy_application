from pydantic import BaseModel


class ContestAddSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    team_1:str
    team_2:str
    series_name:str
    has_mega_contest: bool
    is_contest_open: bool
    deadline: str