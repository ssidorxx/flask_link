from flask import Flask, request, redirect, jsonify, make_response
from flask_jwt_extended import create_access_token, JWTManager,get_jwt_identity, jwt_required
import sqlite3, uuid, pyshorteners, random, hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from server import reg, auth, add_link, update_linkTransitions, delete_link, vivod_links_user, delete_link_transitions, id_user_login
# from flask_sqlalchemy import SQLAlchemy
# from dataclasses import dataclass
# from sqlalchemy.orm import relationship
# import functions

def connect_to_db():
    connect = sqlite3.connect('bdForUP.db', check_same_thread=False)
    return connect

def create_db_table():
    try:
        connect = connect_to_db()
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
        	"id"	INTEGER NOT NULL,
        	"login"	TEXT NOT NULL,
        	"password" TEXT NOT NULL,
        	PRIMARY KEY("id" AUTOINCREMENT)
        );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS "links" (
        	"id"	INTEGER NOT NULL,
        	"link" TEXT NOT NULL,
        	"short_link" TEXT NOT NULL,
        	"transitions" TEXT,
        	"type"	INTEGER NOT NULL,
        	"id_user" INTEGER NOT NULL,
        	PRIMARY KEY("id" AUTOINCREMENT)
        );""")
        #"abbreviated_link" TEXT NOT NULL,
        connect.commit()
        print("User table created successfully")
    except:
        print("User table creation failed - Maybe table")
    finally:
        connect.close()


# Создание таблиц
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
jwt = JWTManager(app)

# @app.route("/")
# def hello_world():
#
#     return "<p>Hello, World!</p>"

#регистрация
@app.route("/reg", methods =['POST'])
def reg_user():
    login = str(request.json.get('login', None))
    password = str(request.json.get('password', None))

    if reg(login, password):
        return make_response("Пользователь успешно зарегистирован")
    else:
        return make_response("Невозможно зарегистрировать этого пользователя")

#аутентификация
@app.route("/auth", methods=['POST'])
def auth_user():
    login = str(request.json.get('login', None))
    password = str(request.json.get('password', None))
    print("m_1")
    if auth(login, password):
        print("m_2")
        token = create_access_token(identity=login)
        return make_response({"token":token})
    else:
        return make_response({"error":"Неверный логин или пароль"})

#сокращение ссылки авторизированного пользователя
@app.route("/add_link", methods=['POST'])
@jwt_required()
def add__link():
    print("я дошел")
    login = str(get_jwt_identity())
    # print (login)
    u_login = id_user_login(login)
    full_link = str(request.json.get("full_link", None))
    transitions = str(request.json.get("transitions", None))
    short_link = pyshorteners.Shortener().clckru.short(full_link)
    access = 1
    if add_link(full_link, short_link, transitions, access, u_login):
        return make_response({"Данная сокр. ссылка добавлена в базу": short_link})
    else:
        return make_response({"error":"возникли проблемы с добавлением"})

#сокращение ссылки
@app.route("/short_link", methods=['POST'])
def short_links():
    full_link = str(request.json.get("full_link", None))
    # short_link = hashlib.md5(full_link.encode()).hexdigest()[:random.randint(8, 12)]
    short_link = pyshorteners.Shortener().clckru.short(full_link)
    return short_link

#все ссылки пользователя
@app.route("/all_links_user", methods=['POST'])
@jwt_required()
def all_links_user():
    login = str(get_jwt_identity())
    # print (login)
    id_user = id_user_login(login)
    links = vivod_links_user(id_user)

    return make_response(f"Юзер: {id_user}, Ссылки: {links}")

#Обновление псевдонима ссылки
@app.route("/update_transitions", methods=['POST'])
def update_transitions():
    id_link = int(request.json.get("id_link", None))
    new_name = str(request.json.get("new_name", None))
    if update_linkTransitions(id_link, new_name):
        return make_response(f"Новый псевдоним ссылки {new_name}")
    else:
        return make_response("error: не удалось обновить псевдоним")

#удаление псевдонима ссылки
@app.route("/delete_transitions", methods=['POST'])
def delete_transitions():
    id_link = str(request.json.get("id_link", None))

    if delete_link_transitions(id_link):
        return make_response("Псевдоним успешно удален")
    else:
        return make_response({"error": "не удалось удалить псевдоним"})

#удаление ссылки
@app.route("/delete_links", methods=['POST'])
def delete_links():
    id_link = str(request.json.get("id_link", None))

    if delete_link(id_link):
        return make_response("Ccылка успешно удалена")
    else:
        return make_response({"error": "не удалось удалить ссылку"})

if __name__=='__main__':
    create_db_table()
    app.run()





