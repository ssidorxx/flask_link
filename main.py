from flask import Flask, request, redirect, jsonify, make_response
from flask_jwt_extended import create_access_token, JWTManager,get_jwt_identity, jwt_required
import sqlite3, uuid, hashlib, random
from werkzeug.security import generate_password_hash, check_password_hash
from server import reg, auth
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS "access" (
        	"id"	INTEGER NOT NULL,
        	"type"	INTEGER NOT NULL,
        	"id_link"	TEXT NOT NULL,
        	"id_user" INTEGER NOT NULL,
        	PRIMARY KEY("id" AUTOINCREMENT)
        );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS "links" (
        	"id"	INTEGER NOT NULL,
        	"link" TEXT NOT NULL,
        	"abbreviated_link" TEXT NOT NULL,
        	"transitions" INTEGER,
        	PRIMARY KEY("id" AUTOINCREMENT)
        );""")

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

@app.route("/")
def hello_world():

    return "<p>Hello, World!</p>"

@app.route("/reg", methods =['POST'])
def reg_user():
    login = str(request.json.get('login', None))
    password = str(request.json.get('password', None))

    if reg(login, password):
        return make_response("Пользователь успешно зарегистирован")
    else:
        return make_response("Невозможно зарегистрировать этого пользователя")


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

@app.route("/auth", methods=['POST'])
def auth_user():

if __name__=='__main__':
    create_db_table()
    app.run()





