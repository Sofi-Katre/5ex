from fastapi import FastAPI, HTTPException, Depends, Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from auth import auth_handler
import bcrypt
import logging
from datetime import datetime
from datetime import datetime as dt

app=FastAPI()
# Вход
@app.post("/login")
def user_auth(login: pyd.LoginUser, db: Session=Depends(get_db)):
    user_db = db.query(m.User).filter(
        m.User.username == login.username
    ).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден!")
    if auth_handler.verify_password(login.password_hash, user_db.password_hash):
        logging.info(f"{dt.now()} - User: {user_db.username} loggined")
        return {"token": auth_handler.encode_token(user_db.id, user_db.role_id, user_db.username)}
    logging.info(f"{dt.now()} - User: {user_db.username} fail authentication")
    raise HTTPException(400, "Доступ запрещён!")
# Статьи
# Получение статьи
@app.get("/api/ads", response_model=List[pyd.SchemeAd])
def get_ads(limit:None|int=Query(None, le=100), page:None|int=Query(1), category:None|str=Query(None), db:Session=Depends(get_db)):
    ads = db.query(m.Ad)
    if category:
        category_db = db.query(m.Category).filter(
            m.Category.name == category
        ).first()
        if not category_db:
            raise HTTPException(404, "Категория не найдена!")
        ads = ads.filter(
            m.Ad.category_id == category_db.id
        )
    if limit:
        ads = ads[(page - 1) * limit:page * limit]
        if not ads:
            raise HTTPException(404, "Статьи не найдены!")
        return ads
    all_ads = ads.all()
    if not all_ads:
        raise HTTPException(404, "Статьи не найдены!")
    return all_ads

# Создание статьи
@app.post("/api/ad", response_model=pyd.SchemeAd)
def create_Ad(Ad:pyd.CreateAd, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Ad_dublicate = db.query(m.Ad).filter(
        m.Ad.title == Ad.title
    ).first()
    if Ad_dublicate:
        raise HTTPException(400, "Такая статья уже существует!")
    Ad_db = m.Ad()
    Ad_db.title = Ad.title
    Ad_db.category_id = Ad.category_id
    Ad_db.description = Ad.description
    Ad_db.price = Ad.price
    Ad_db.dateT = datetime.now()
    Ad_db.author_id = Ad.author_id

    db.add(Ad_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} create product: {Ad_db.title}")
    return Ad_db

# Получение 1 статьи
@app.get("/api/ad/{id}", response_model=pyd.SchemeAd)
def get_Ad(id:int, db:Session=Depends(get_db)):
    Ad_db = db.query(m.Ad).filter(
        m.Ad.id == id
    ).first()
    if not Ad_db:
        raise HTTPException(404, "Статья не найдена!")
    return Ad_db

# Изменение статьи
@app.put("/api/ad/{id}", response_model=pyd.SchemeAd)
def edit_Ad(id:int, Ad:pyd.CreateAd, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Ad_db = db.query(m.Ad).filter(
        m.Ad.id == id
    ).first()
    if not Ad_db:
        raise HTTPException(404, "Статья не найдена!")
    Ad_db.title = Ad.title
    Ad_db.category_id = Ad.category_id
    Ad_db.description = Ad.description
    Ad_db.price = Ad.price
    Ad_db.dateT = datetime.now()
    Ad_db.author_id = Ad.author_id

    db.add(Ad_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} change product: {Ad_db.title}")
    return Ad_db

# Удаление статьи
@app.delete("/api/ad/{id}")
def delete_ad(id:int, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Ad_db = db.query(m.Ad).filter(
        m.Ad.id == id
    ).first()
    if not Ad_db:
        raise HTTPException(404, "Статья не найдена!")
    db.delete(Ad_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} delete product: {Ad_db.title}")
    return {"detail": "Статья удалена!"}

# Создание категории
@app.post("/api/сategory", response_model=pyd.BaseCategory)
def create_Сategory(Сategory:pyd.CreateCategory, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Category_dublicate = db.query(m.Category).filter(
        m.Category.name == Сategory.name
    ).first()
    if Category_dublicate:
        raise HTTPException(400, "Такая категория уже существует!")
    Category_db = m.Сategory()
    Category_db.name = Сategory.name

    db.add(Category_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} create product: {Category_db.name}")
    return Category_db

# Изменение категории
@app.put("/api/сategory/{id}", response_model=pyd.BaseCategory)
def edit_Сategory(id:int, Сategory:pyd.CreateCategory, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Сategory_db = db.query(m.Сategory).filter(
        m.Сategory.id == id
    ).first()
    if not Сategory_db:
        raise HTTPException(404, "Категория не найдена!")
    Category_db = m.Сategory()
    Category_db.name = Сategory.name

    db.add(Сategory_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} change product: {Сategory_db.name}")
    return Сategory_db

# Удаление категории
@app.delete("/api/сategory/{id}")
def delete_сategory(id:int, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Сategory_db = db.query(m.Сategory).filter(
        m.Сategory.id == id
    ).first()
    if not Сategory_db:
        raise HTTPException(404, "Категория не найдена!")
    db.delete(Сategory_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} delete product: {Сategory_db.name}")
    return {"detail": "Статья удалена!"}

# Получение 1 категории
@app.get("/api/сategory/{id}", response_model=pyd.BaseCategory)
def get_Ad(id:int, db:Session=Depends(get_db)):
    Сategory_db = db.query(m.Сategory).filter(
        m.Сategory.id == id
    ).first()
    if not Сategory_db:
        raise HTTPException(404, "Категория не найдена!")
    return Сategory_db

# Создание Отклика
@app.post("/api/response", response_model=pyd.BaseResponse)
def create_Response(Response:pyd.CreateResponse, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Response_dublicate = db.query(m.Category).filter(
        m.Response.message == Response.message
    ).first()
    if Response_dublicate:
        raise HTTPException(400, "Такой отзыв уже существует!")
    Response_db = m.Response()
    Response_db.ad_id = Response.ad_id
    Response_db.user_id = Response.user_id
    Response_db.message = Response.message

    db.add(Response_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} create product: {Response_db.message}")
    return Response_db

# Изменение Отклика
@app.put("/api/response/{id}", response_model=pyd.BaseResponse)
def edit_Response(id:int, Response:pyd.CreateResponse, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Сategory_db = db.query(m.Response).filter(
        m.Response.id == id
    ).first()
    if not Сategory_db:
        raise HTTPException(404, "Отклик не найден!")
    Response_db = m.Response()
    Response_db.ad_id = Response.ad_id
    Response_db.user_id = Response.user_id
    Response_db.message = Response.message

    db.add(Response_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} change product: {Response_db.message}")
    return Response_db

# Удаление Отклика
@app.delete("/api/response/{id}")
def delete_Response(id:int, db:Session=Depends(get_db), moder:m.User=Depends(auth_handler.moder_wrapper)):
    Response_db = db.query(m.Response).filter(
        m.Response.id == id
    ).first()
    if not Response_db:
        raise HTTPException(404, "Отклик не найден!")
    db.delete(Response_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {moder["user_id"]} - {moder["username"]} delete product: {Response_db.message}")
    return {"detail": "Статья удалена!"}

# Получение 1 категории
@app.get("/api/response/{id}", response_model=pyd.BaseResponse)
def get_Ad(id:int, db:Session=Depends(get_db)):
    Response_db = db.query(m.Response).filter(
        m.Response.id == id
    ).first()
    if not Response_db:
        raise HTTPException(404, "Отклик не найден!")
    return Response_db