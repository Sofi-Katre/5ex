from pydantic import BaseModel, Field


class BaseProduct(BaseModel):
    id:int=Field(example=1)
    product_name:str=Field(example='Milk')

class BasePlanet(BaseModel):
    id:int=Field(example=1)
    planet_name:str=Field(example="Земля")
    planet_mass:float=Field(example=5.9)
    planet_diameter:float=Field(example=12756)