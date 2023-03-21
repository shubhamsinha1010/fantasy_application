from typing import Optional
from pydantic import BaseModel


class SignUpSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    username:str
    email:str
    password:str
    friend_referal_code: Optional[str]
    is_above_18: Optional[bool]
    is_staff:Optional[bool]
    is_active:Optional[bool]


    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True,
                "is_above_18": True,
                "friend_referal_code": "qwerty12"
            }
        }


class LoginSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    username: str
    password: str


class TokenSchema(BaseModel):

   token: str