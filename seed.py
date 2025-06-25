from sqlalchemy.orm import Session
from database import engine
import models as m
from datetime import datetime

m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    rol1 = m.Role(rolename="Пользователь")
    session.add(rol1)

    rol2 = m.Role(rolename="Модератор")
    session.add(rol2)

    rol3 = m.Role(rolename="Админ")
    session.add(rol3)

    u1 = m.User(username = "Джин Смит", password_hash = "123", role_id = "1")
    session.add(u1)

    u2 = m.User(username = "Владислав Хам", password_hash = "6849393ham", role_id = "3")
    session.add(u2)

    u3 = m.User(username = "Илья Колот", password_hash = "6843ham", role_id = "2")
    session.add(u3)

    cat1 = m.Category(name = "Машины")
    session.add(cat1)

    cat2 = m.Category(name = "Книги")
    session.add(cat2)

    ad1 = m.Ad(author_id = 1, title = "Убийства в книгах", description = "Как главные персонажи в лице детективов и частных сыщиков раскрывают самые жуткие преступления", category_id = 2, price = 200, date = datetime.strptime("2025-06-25", "%Y-%m-%d").date())
    session.add(ad1)

    ad2 = m.Ad(author_id = 2, title = "Hynday Avante", description = "Какого ездить на корейце с 5 летним пробегом?", category_id = 1, price = 100, date = datetime.strptime("2020-03-01", "%Y-%m-%d").date())
    session.add(ad2)

    res1 = m.Response(ad_id = 1, user_id = 1)
    session.add(res1)

    res2 = m.Response(ad_id = 2, user_id = 2)
    session.add(res2)

    fav1 = m.Favorite(user_id = 1, ad_id = 1)
    session.add(fav1)


    session.commit()