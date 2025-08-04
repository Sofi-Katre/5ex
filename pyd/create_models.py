from pydantic import BaseModel, Field
from datetime import date
import re

class CreateAd(BaseModel):
    author_id:int=Field(example="1")
    title:str=Field(example="Убийство на молочной ферме", min_length=2)
    description:str|None=Field(example="Описание", default=None)
    category_id:int=Field(example="2")
    price:float=Field(example="200")

class CreateCategory(BaseModel):
    name:str=Field(example='Еда')

class CreateResponse(BaseModel):
    ad_id:int=Field(example="1")
    user_id:int=Field(example="1")
    message:str=Field(example="Убийство на молочной ферме", min_length=2)

class LoginUser(BaseModel):
    username:str=Field(example="Поала", min_length=2, max_length=20)
    password_hash:str=Field(example="Пладула112у", min_length=8, max_length=20, pattern=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"))