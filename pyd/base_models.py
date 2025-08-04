from pydantic import BaseModel, Field
from datetime import date


class BaseRole(BaseModel):
    id:int=Field(example=1)
    rolename:str=Field(example='Админ')

class BaseUser(BaseModel):
    id:int=Field(example=1)
    username:str=Field(example='Владислав')

class BaseCategory(BaseModel):
    id:int=Field(example=1)
    name:str=Field(example='Книги')   

class BaseAd(BaseModel):
    id:int=Field(example=1)
    title:str=Field(example="Убийства в книгах")
    description:str=Field(example="Какого ездить на корейце с 5 летним пробегом?")
    price:float=Field(example=509)
    dateT:date=Field(example="2025-06-25")

class BaseResponse(BaseModel):
    id:int=Field(example=1)
    message:str=Field(example='Хей, крутая статья!')

class BaseFavorite(BaseModel):
    id:int=Field(example=1)