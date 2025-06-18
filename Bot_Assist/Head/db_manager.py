import sqlite3
from itertools import *


# ДОБАВЛЯЕТ В БД ПОЛЬЗОВАТЕЛЯ
def db_users_add(id_telegram,reg_info,username):
    second_name, first_name, patronymic = reg_info.split()

    path = r'Bot_Assist/Head/Data_Base/users_base.db'

    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        id_telegram INTEGER,
        second_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        patronymic TEXT NOT NULL,
        username TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()

    for user in users:
        if user[1] == id_telegram:
            return 0

    cursor.execute('''INSERT INTO Users(id_telegram,second_name,first_name,patronymic,username) VALUES(?,?,?,?,?)''',(f'{id_telegram}',f'{second_name}',f'{first_name}',f'{patronymic}',f'{username}'))
    connection.commit()
    connection.close()

    db_users_table_add(id_telegram)

    return 1

# СОЗДАЕТ ДЛЯ ПОЛЬЗОВАТЕЛЯ БД ЗАДАНИЙ
def db_users_table_add(id_user):
    path = fr'Bot_Assist/Head/Data_Base/user_db/{id_user}.db'

    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute('''
           CREATE TABLE IF NOT EXISTS tasks (
           id INTEGER PRIMARY KEY,
           name STRING TEXT NOT NULL,
           description TEXT NOT NULL,
           date TEXT NOT NULL,
           id_user INTEGER
           )
       ''')

    connection.commit()
    connection.close()

# ДОБАВЛЯЕТ ЗАДАНИЕ ПОЛЬЗОВАТЕЛЮ
def db_user_task_add(task):
    name,description,date,id_users = task

    for id_user in id_users:
        path = fr'Bot_Assist/Head/Data_Base/user_db/{id_user}.db'

        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name STRING TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            id_user INTEGER
            )
        ''')
        try:
            cursor.execute('''INSERT INTO tasks(name,description,date,id_user) VALUES(?,?,?,?)''',(f'{name}',f'{description}',f'{date}',f'{id_user}'))
            connection.commit()
            connection.close()
            return 1
        except:
            return 0

# ВЫВОДИТ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
def db_users_check(info: str = 'name'):
    path = r'Bot_Assist/Head/Data_Base/users_base.db'

    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        id_telegram INTEGER,
        second_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        patronymic TEXT NOT NULL,
        username TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()

    user_info = []

    if info == 'name':
        for user in users:
            user_info.append(user[2:4])
        return user_info
    elif info == 'id':
        for user in users:
            user_info.append(user[1])
        return user_info
    elif info == 'num_name':
        for user in users:
            user_info.append([user[0],user[2],user[3]])
        return user_info

# ВЫВОДИТ ВСЕ ЗАДАНИЯ ПОЛЬЗОВАТЕЛЯ
def db_user_task_check(id_user):
    path = fr'Bot_Assist/Head/Data_Base/user_db/{id_user}.db'

    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name STRING TEXT NOT NULL,
        description TEXT NOT NULL,
        date TEXT NOT NULL,
        id_user INTEGER
        )
    ''')

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    return tasks

def db_user_num_to_id(num_performer: str = '-1',id:bool = 0):
    path = r'Bot_Assist/Head/Data_Base/users_base.db'

    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        id_telegram INTEGER,
        second_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        patronymic TEXT NOT NULL,
        username TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()

    if id == 0:
        if num_performer.count('/')==0:
            for user in users:
                if user[0] == int(num_performer):
                    return [user[2:4]]
        else:
            name_performers = []
            num_performers = num_performer.split('/')
            for num in num_performers:
                for user in users:
                    if user[0] == int(num):
                        name_performers.append(user[2:4])
            return name_performers
    if id == 1:
        if num_performer.count('/')==0:
            for user in users:
                if user[0] == int(num_performer):
                    return [user[1]]
        else:
            id_performers = []
            num_performers = num_performer.split('/')
            for num in num_performers:
                for user in users:
                    if user[0] == int(num):
                        id_performers.append(user[1])
            return id_performers