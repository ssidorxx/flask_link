import sqlite3, hashlib, random

def connect_to_db():
    try:
        connect = sqlite3.connect('bdForUP.db', check_same_thread=False)
        return connect
    except sqlite3.Error as err:
        print(err)

# регистрация +
def reg(u_login, u_password):
    try:

        connect = connect_to_db()
        cursor = connect.cursor()

        cursor.execute(f"SELECT login FROM users WHERE login=?",(u_login,))
        # connect.commit()

        if cursor.fetchone() is None:
            print("1")
            cursor.execute(f"INSERT INTO users(login, password) VALUES('{u_login}','{u_password}')")
            print("2")
            connect.commit()
            print("вы успешно зарегистрировались!")
            return True;
        else:
            print("такая запись уже есть!")
            return False;
        # connect.commit()

        print("Отработано")
    except:
        print("Ошибка")
    finally:
        connect.close()

# аутентификация +
def auth(u_login, u_password):
    print("0")
    connect = connect_to_db()
    cursor = connect.cursor()
    print("1")
    cursor.execute(f"SELECT * FROM users WHERE login=:login AND password=:password", {"login": u_login, "password": u_password})

    connect.commit()
    print("2")
    if cursor.fetchall() is None:
        return False;
        print("Неверный логин или пароль")
    else:
        return True;
        print("Вы успешно вошли")

#добавление ссылки в базу +
def add_link(u_link, short_link, transitions, type, login):
     try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT link FROM links WHERE link=:link AND id_user=:id_user",{"link": u_link, "id_user": login,})
        connect.commit()
        print("2")
        # print(cursor.fetchall())
        # print(cursor.fetchall() is None)
        if cursor.fetchall() == []:
            # запрос на добавлени информации о ссылке
            print("3")
            cursor.execute(f"INSERT INTO links (link, short_link, transitions, type, id_user) VALUES(:link, :short_link, :transitions, :type, :id_user)",
             {"link": u_link, "short_link": short_link,"transitions": transitions, "type": type, "id_user": login})
            connect.commit()
            print("Ссылка успешно добавлена")
            # возвращаем объект
            return True;

        else:
            return False;
            print("у вас уже есть данная ссылка")
     except:
        print("Ошибка")
     finally:
        connect.close()

# добавление псевонима (?)
def add_linkTransitions(transitions, id):
    try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT id FROM links WHERE login=?", (id,))
        connect.commit()
        print("2")
        if cursor.fetchall() is None:
            # запрос на добавлени информации о ссылке
            (f"INSERT INTO links (transitions) VALUES(:transitions) WHERE id=:id",
             {"transitions": transitions, "id": id})
            connect.commit()
            print("Псевдоним успешно добавлен")
            # возвращаем объект
            return True;

        else:
            return False;
            print("не удалось добавить псевдоним ссылке")
    except:
        print("Ошибка")
    finally:
        connect.close()

# обновление псевдонима +
def update_linkTransitions(id, transitions):
    try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT id FROM links WHERE id=:id", {"id":id})
        connect.commit()
        print("2")
        if cursor.fetchall() is not None:
            # запрос на изменение псевдонима ссылки
            cursor.execute(f"UPDATE links SET transitions=:transitions WHERE id=:id", {"transitions": transitions, "id": id} )
            connect.commit()
            print("Псевдоним успешно обновлен")
            return True;
        else:
            return False;
            print("не удалось найти ссылку")
    except:
        print("Ошибка")
    finally:
        connect.close()

# удаление псевдонима ссылки +
def delete_link_transitions(id):
    try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT id FROM links WHERE id=:id", {"id":id})
        connect.commit()
        print(cursor.fetchall())
        if cursor.fetchall() is not None:
            # запрос на удаление псевдонима ссылки
            cursor.execute(f"UPDATE links SET transitions=:transitions WHERE id=:id", {"transitions": "", "id": id} )
            connect.commit()
            print("Псевдоним успешно удален")
            return True;
        else:
            return False;
            print("не удалось найти ссылку")
    except:
        print("Ошибка")
    finally:
        connect.close()

# удаление ссылки
def delete_link(id):
    try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT id FROM links WHERE id=:id", {"id":id})
        connect.commit()
        print(cursor.fetchall())
        if cursor.fetchall() is not None:
            # запрос на удаление ссылки
            print("2")
            cursor.execute(f"DELETE FROM links WHERE id=:id", {"id": id})
            connect.commit()
            print("Ссылка успешно удалена")
            return True;
        else:
            return False;
            print("не удалось найти ссылку")
    except:
        print("Ошибка")
    finally:
        connect.close()

# вывод всех ссылок пользователя +
def vivod_links_user(id_user,):
    try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT id_user FROM links WHERE id_user=:id_user", {"id_user":id_user})
        connect.commit()
        if cursor.fetchall() == []:
            return False;
            print("не удалось найти ссылок у этого пользователя")
        else:
            print("2")
            # запрос на вывод всех ссылок по пользователю
            cursor.execute(f"SELECT id, transitions, short_link FROM links WHERE id_user=:id_user", {"id_user": id_user})
            connect.commit()
            m = cursor.fetchall()
            return m;
    except:
        print("Ошибка")
    finally:
        connect.close()

# вывод основной ссылки по превдониму
def vivod_main_links_user(id_user, transitions, ):
    try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT id_link FROM access WHERE id_user=?", (id_user,))
        connect.commit()
        print("2")
        if cursor.fetchall() is None:
            return False;
            print("не удалось найти ссылок у этого пользователя")
        else:
            # запрос на вывод всех ссылок по пользователю
            (f"SELECT abbreviated_link FROM links INNER JOIN access ON links.id = access.id_link WHERE access.id_user=:id_user and links.transitions=:transitions ", {"id_user": id_user, "transitions": transitions})
            connect.commit()
            print("Основная сcылка успешно возвращена")
            m = cursor.fetchone()
            return m;
    except:
        print("Ошибка")
    finally:
        connect.close()

def id_user_login(login):
    try:
        print("0")
        connect = connect_to_db()
        cursor = connect.cursor()
        print("1")
        cursor.execute(f"SELECT id FROM users WHERE login=:login", {"login": login})
        connect.commit()
        m = cursor.fetchall()
        print(m)
        return m[0][0]

        # if cursor.fetchall() is None:
        #     return False;
        #     print("не удалось найти ссылок у этого пользователя")
        # else:
        #     # запрос на вывод всех ссылок по пользователю
        #     (f"SELECT abbreviated_link FROM links INNER JOIN access ON links.id = access.id_link WHERE access.id_user=:id_user and links.transitions=:transitions ", {"id_user": id_user, "transitions": transitions})
        #     connect.commit()
        #     print("Основная сcылка успешно возвращена")
        #     m = cursor.fetchone()
        #     return m;
    except:
        print("Ошибка")
    finally:
        connect.close()