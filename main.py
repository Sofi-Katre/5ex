from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd


app=FastAPI()

# Продукты
@app.get('/products', response_model=List[pyd.BaseProduct])
def get_all_products(db:Session=Depends(get_db)):
    products = db.query(m.Product).all()
    return products

@app.get("/product/{product_id}", response_model=pyd.BaseProduct)
def get_planet(product_id:int, db:Session=Depends(get_db)):
    product = db.query(m.Product).filter(
        m.Product.id==product_id
    ).first()
    if not product:
        raise HTTPException(404, 'Товар не найден')
    return product

@app.post("/product", response_model=pyd.BaseProduct)
def create_product(product:pyd.CreateProduct, db:Session=Depends(get_db)):
    product_db = m.Product()
    product_db.product_name = product.product_name

    db.add(product_db)
    db.commit()
    return product_db

@app.delete("/product/{product_id}")
def delete_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(m.Product).filter(
        m.Product.id==product_id
    ).first()
    if not product:
        raise HTTPException(404, 'Товар не найден')
    db.delete(product)
    db.commit()
    return {'detail': "Товар удалён"}

# Планеты
@app.get("/planets", response_model=List[pyd.BasePlanet])
def get_all_planets(db:Session=Depends(get_db)):
    planets = db.query(m.Planet).all()
    return planets

@app.get("/planet/{planet_id}", response_model=pyd.BasePlanet)
def get_planet(planet_id:int, db:Session=Depends(get_db)):
    planet = db.query(m.Planet).filter(
        m.Planet.id==planet_id
    ).first()
    if not planet:
        raise HTTPException(404, 'Планета не найдена')
    return planet

@app.post("/planet", response_model=pyd.BasePlanet)
def create_planet(planet:pyd.CreatePlanet, db:Session=Depends(get_db)):
    planet_db = m.Planet()

    planet_db.planet_name = planet.planet_name
    planet_db.planet_mass = planet.planet_mass
    planet_db.planet_diameter = planet.planet_diameter

    db.add(planet_db)
    db.commit()
    return planet_db

@app.delete("/planet/{planet_id}")
def delete_product(planet_id:int, db:Session=Depends(get_db)):
    planet = db.query(m.Planet).filter(
        m.Planet.id==planet_id
    ).first()
    if not planet:
        raise HTTPException(404, 'Планета не найдена')
    db.delete(planet)
    db.commit()
    return {'detail': "Планета удалена"}
#
