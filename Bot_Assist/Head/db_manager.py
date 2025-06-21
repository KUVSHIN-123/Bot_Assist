import sqlite3

path_users_db = r'/home/main_server/Bot_Assist/Bot_Assist/Head/Data_Base/users_base.db'
path_tasks_db = r'/home/main_server/Bot_Assist/Bot_Assist/Head/Data_Base/user_db/'

db_users = ''' 
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        id_telegram INTEGER,
        second_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        patronymic TEXT NOT NULL,
        username TEXT NOT NULL
        )
    '''
db_tasks = '''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name STRING TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            num_performers TEXT NOT NULL,
            id_task TEXT NOT NULL,
            status STRING TEXT NOT NULL
            )
        '''

# ДОБАВЛЯЕТ В БД ПОЛЬЗОВАТЕЛЯ
def db_users_add(id_telegram,reg_info,username): # ПРИНИМАЕТ ID ПОЛЬЗОВАТЕЛЯ, ИНФОРМАЦИЮ КОТОРУЮ ВВЁЛ ПОЛЬЗОВАТЕЛЬ, USERNAME ПОЛЬЗОВАТЕЛЯ (МОЖЕТ ОТСУТСТВОВАТЬ)
    second_name, first_name, patronymic = reg_info.split()  # РАЗДЕЛЯЕТ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ

    connection = sqlite3.connect(path_users_db)             # ОТКРЫВАЕТ СОЕДИНЕНИЕ
    cursor = connection.cursor()                            # СОЗДАНИЕ КУРСОРА
    cursor.execute(db_users)                                # СОЗДАЕТ БД ЕСЛИ ЕЁ НЕТ
    cursor.execute('SELECT * FROM Users')                   # ВЫБИРАЕТ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
    users = cursor.fetchall()                               # ПЕРЕМЕННАЯ users ПРИНИМАЕТ ДАННЫЕ О ВСЕХ ПОЛЬЗОВАТЕЛЯХ

    for user in users:                                      # ПЕРЕБОР ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
        if user[1] == id_telegram:                          # ЕСЛИ ПОЛЬЗОВАТЕЛЬ УЖЕ ЕСТЬ В БД
            return 0

    # ДОБАВЛЯЕМ НОВОГО ПОЛЬЗОВАТЕЛЯ В БД
    cursor.execute('''INSERT INTO Users(id_telegram,second_name,first_name,patronymic,username) VALUES(?,?,?,?,?)''',(f'{id_telegram}',f'{second_name}',f'{first_name}',f'{patronymic}',f'{username}'))
    connection.commit()                                     # СОХРАНЯЕМ ИЗМЕНЕНИЯ
    connection.close()                                      # ЗАКРЫВАЕМ СОЕДИНЕНИЕ
    db_users_table_add(id_telegram)                         # ВЫЗЫВАЕМ ФУНКЦИЮ ДЛЯ СОЗДАНИЯ БД ЗАДАНИЙ ПОЛЬЗОВАТЕЛЯ
    return 1

# СОЗДАЕТ ДЛЯ ПОЛЬЗОВАТЕЛЯ БД ЗАДАНИЙ
def db_users_table_add(id_user): # ПРИНИМАЕТ ID ПОЛЬЗОВАТЕЛЯ

    connection = sqlite3.connect(fr"{path_tasks_db}{id_user}.db")   # ОТКРЫВАЕМ СОЕДИНЕНИЕ
    cursor = connection.cursor()                                    # СОЗДАЕМ КУРСОР
    cursor.execute(db_tasks)                                        # СОЗДАЕМ БД ЕСЛИ ЕЁ НЕТ
    connection.commit()                                             # СОХРАНЯЕМ ИЗМЕНЕНИЯ
    connection.close()                                              # ЗАКРЫВАЕМ СОЕДИНЕНИЕ

# ДОБАВЛЯЕТ ЗАДАНИЕ ПОЛЬЗОВАТЕЛЮ
def db_user_task_add(task): # ПРИНИМАЕТ СПИСОК ДАННЫХ О ЗАДАНИИ
    name,description,date,id_users,num_performers,id_task = task #РАЗДЕЛЯЕМ ДАННЫЕ О ЗАДАНИИ
    # (НАЗВАНИЕ, ОПИСАНИЕ, СРОК ИСПОЛНЕНИЯ, ID ТЕХ КОМУ ДАНО ЗАДАНИЕ, ПОРЯДКОВЫЙ НОМЕР ТЕХ КОМУ ДАНО ЗАДАНИЕ, ID ЗАДАНИЯ СОБРАННОЕ ИЗ ВРЕМЕНИ В МОМЕНТ ДАЧИ ЗАДАНИЯ)

    for id_user in id_users:                                            # ПЕРЕБИРАЕМ КАЖДЫЙ ID ПОЛЬЗОВАТЕЛЯ ЧТО БЫ ДАТЬ ЗАДАНИЕ
        connection = sqlite3.connect(fr"{path_tasks_db}{id_user}.db")   # ОТКРЫВАЕМ СОЕДИНЕНИЕ
        cursor = connection.cursor()                                    # СОЗДАЕМ КУРСОР
        cursor.execute(db_tasks)                                        # СОЗДАЕМ БД ЗАДАНИЙ ЕСЛИ ЕЁ НЕТ
        status = 'ACTIVE'                                               # ИЗНАЧАЛЬНЫЙ СТАТУС ЗАДАНИЯ

        # ДОБАВЛЯЕМ В БД ЗАДАНИЕ
        cursor.execute('''INSERT INTO tasks(name,description,date,num_performers,id_task,status) VALUES(?,?,?,?,?,?)''',(f'{name}',f'{description}',f'{date}',f'{num_performers}',f'{id_task}',f'{status}'))
        connection.commit() # СОХРАНЯЕМ ИЗМЕНЕНИЯ
        connection.close()  # ЗАКРЫВАЕМ СОЕДИНЕНИЕ

    return 1

# МЕНЯЕТ СТАТУС ЗАДАНИЯ НА "COMPLETE"
def db_user_task_edit(id_users,id_task): # ПРИНИМАЕТ ID ВСЕХ ПОЛЬЗОВАТЕЛЕЙ, ID ЗАДАНИЯ
    for id_user in id_users: # ПЕРЕБИРАЕТ КАЖДЫЙ ID

        new_status = 'COMPLETE'                                         # НОВЫЙ СТАТУС ЗАДАНИЯ
        connection = sqlite3.connect(fr"{path_tasks_db}{id_user}.db")   # ОТКРЫВАЕМ СОЕДИНЕНИЕ
        cursor = connection.cursor()                                    # СОЗДАЕМ КУРСОР
        cursor.execute(db_tasks)                                        # СОЗДАЕМ БД ЕСЛИ ЕЁ НЕТ

        # МЕНЯЕМ СТАТУС У ТЕХ ЗАДАНИЙ ID КОТОРЫХ СООТВЕТСТВУЕТ ТРЕБУЕМОМУ
        cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id_task = ?
        """, (new_status, id_task))
        connection.commit()                                             # СОХРАНЯЕМ ИЗМЕНЕНИЯ
        connection.close()                                              # ЗАКРЫВАЕМ СОЕДИНЕНИЕ

    return 1

# ВЫВОДИТ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
def db_users_check(info: str = 'name'): # ПРИНИМАЕТ ПАРАМЕТР info, ИЗНАЧАЛЬНО ПАРАМЕТР = name

    connection = sqlite3.connect(path_users_db)         # ОТКРЫВАЕМ СОЕДИНЕНИЕ
    cursor = connection.cursor()                        # СОЗДАЕМ КУРСОР
    cursor.execute(db_users)                            # СОЗДАЕТ БД ЕСЛИ ЕЁ НЕТ

    cursor.execute('SELECT * FROM Users')               # ВЫБИРЕМ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
    users = cursor.fetchall()                           # ПЕРЕМЕННАЯ users ПРИНИМАЕТ ДАННЫЕ О ВСЕХ ПОЛЬЗОВАТЕЛЯХ

    user_info = []                                      # СПИСОК В КОТОРЫЙ БУДЕТ ЗАПИСАН РЕЗУЛЬТАТ РАБОТЫ ФУНКЦИИ

    if info == 'name':                                  # ЕСЛИ ПАРАМЕТР name ТО ЗАПИСЫВАЕМ фамилию и имя КАЖДОГО ПОЛЬЗОВАТЕЛЯ
        for user in users:
            user_info.append(user[2:4])                 # [2] = фамилия  [3] = имя
        return user_info
    elif info == 'id':                                  # ЕСЛИ ПАРАМЕТР id ТО ЗАПИСЫВАЕМ id_telegram КАЖДОГО ПОЛЬЗОВАТЕЛЯ
        for user in users:
            user_info.append(user[1])                   # [1] = id_telegram
        return user_info
    elif info == 'num_name':                            # ЕСЛИ ПАРАМЕТР num_name ТО ЗАПИСЫВАЕМ порядковый номер, фамилию и имя КАЖДОГО ПОЛЬЗОВАТЕЛЯ
        for user in users:
            user_info.append([user[0],user[2],user[3]]) # [0] = порядковый номер [2] = фамилия  [3] = имя
        return user_info
    elif info == 'name_id':                             # ЕСЛИ ПАРАМЕТР name_id ТО ЗАПИСЫВАЕМ id_telegram, фамилию и имя КАЖДОГО ПОЛЬЗОВАТЕЛЯ
        for user in users:
            user_info.append([user[1],user[2],user[3]]) # [1] = id_telegram [2] = фамилия  [3] = имя
        return user_info
    elif info == 'num_id':                              # ЕСЛИ ПАРАМЕТР num_id ТО ЗАПИСЫВАЕМ порядковый номер и id_telegram КАЖДОГО ПОЛЬЗОВАТЕЛЯ
        for user in users:
            user_info.append([user[0],user[1]])         # [0] = порядковый номер [1] = id_telegram
        return user_info

# ВЫВОДИТ ВСЕ ЗАДАНИЯ ПОЛЬЗОВАТЕЛЯ
def db_user_task_check(id_users: list = [],info: str ='all'): # ПРИНИМАЕТ СПИСОК ID ПОЛЬЗОВАТЕЛЕЙ, ПАРАМЕТР info, ИЗНАЧАЛЬНО ПАРАМЕТР = all
    for id_user in id_users:                                            # ПЕРЕБИРАЕТ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ

        connection = sqlite3.connect(fr"{path_tasks_db}{id_user}.db")   # ОТКРЫВАЕМ СОЕДИНЕНИЕ
        cursor = connection.cursor()                                    # СОЗДАЕМ КУРСОР
        cursor.execute(db_tasks)                                        # СОЗДАЕМ БД ЕСЛИ ЕЁ НЕТ

    if info == 'all':                                                   # ЕСЛИ ПАРАМЕТР all ТО ВОЗВРАЩАЕМ ВСЕ ЗАДАНИЯ ПОЛЬЗОВАТЕЛЯ
        cursor.execute('''
                       SELECT *
                       FROM tasks
                       ''')
        tasks = cursor.fetchall()
        return tasks
    elif info == 'active':                                              # ЕСЛИ ПАРАМЕТР active ТО ВОЗВРАЩАЕМ ТОЛЬКО АКТИВНЫЕ ЗАДАНИЯ ПОЛЬЗОВАТЕЛЯ
        cursor.execute('''
                       SELECT *
                       FROM tasks
                       WHERE status = 'ACTIVE'
                       ''')
        tasks = cursor.fetchall()
        return tasks
    elif info == 'complete':                                            # ЕСЛИ ПАРАМЕТР complete ТО ВОЗВРАЩАЕМ ТОЛЬКО ВЫПОЛНЕННЫЕ ЗАДАНИЯ ПОЛЬЗОВАТЕЛЯ
        cursor.execute('''
                       SELECT *
                       FROM tasks
                       WHERE status = 'COMPLETE'
                       ''')
        tasks = cursor.fetchall()
        return tasks

# ВОЗВРАЩАЕТ ИМЯ ПОЛЬЗОВАТЕЛЕ ИЛИ ID ПОЛЬЗОВАТЕЛЕЙ, ИЩЕТ ИХ ПО СПИСКУ НОМЕРОВ ПОЛЬЗОВАТЕЛЯ
def db_user_num_to_id(num_performer: str = '-1',id:bool = 0): # ПРИНИМАЕТ порядковые номера ПОЛЬЗОВАТЕЛЕЙ ПО ФОРМАТУ "1/2/3/4", ПАРАМЕТР id, ИЗНАЧАЛЬНО ПАРАМЕТР = 0

    connection = sqlite3.connect(path_users_db)         # ОТКРЫВАЕМ СОЕДИНЕНИЕ
    cursor = connection.cursor()                        # СОЗДАЕМ КУРСОР
    cursor.execute(db_users)                            # СОЗДАЕТ БД ЕСЛИ ЕЁ НЕТ
    cursor.execute('SELECT * FROM Users')               # ВЫБИРАЕТ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
    users = cursor.fetchall()                           # ПЕРЕМЕННАЯ users ПРИНИМАЕТ ДАННЫЕ О ВСЕХ ПОЛЬЗОВАТЕЛЯХ

    if id == 0:                                         # ЕСЛИ ПАРАМЕТР id = 0, ТО БУДЕМ ВОЗВРАЩАТЬ фамилию и имя ПОЛЬЗОВАТЕЛЯ
        if num_performer.count('/')==0:                 # ЕСЛИ ЗАДАНИЕ ДАНО ТОЛЬКО ОДНОМУ ПОЛЬЗОВАТЕЛЮ
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
    if id == 1:                                         # ЕСЛИ ПАРАМЕТР id = 1, ТО БУДЕМ ВОЗВРАЩАТЬ id ПОЛЬЗОВАТЕЛЯ
        if num_performer.count('/')==0:                 # ЕСЛИ ЗАДАНИЕ ДАНО ТОЛЬКО ОДНОМУ ПОЛЬЗОВАТЕЛЮ
            for user in users:
                if user[0] == int(num_performer):
                    return [user[1]]
        elif num_performer.count('/')>0:
            id_performers = []
            num_performers = num_performer.split('/')
            for num in num_performers:
                for user in users:
                    if user[0] == int(num):
                        id_performers.append(user[1])
            return id_performers