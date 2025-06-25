from pydantic import BaseModel, Field


class CreateProduct(BaseModel):
    product_name:str=Field(min_length=3, max_length=30, example='Milk')


class CreatePlanet(BaseModel):
    planet_name:str=Field(min_length=3, max_length=50, example="Земля")
    planet_mass:float=Field(example=5.9)
    planet_diameter:float=Field(example=12756)