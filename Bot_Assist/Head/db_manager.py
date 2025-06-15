import sqlite3

def data_base_writer(id_telegram,reg_info,username):
    connection = sqlite3.connect(r'Bot_Assist/Head/DataBase.db')
    cursor = connection.cursor()

    second_name, first_name, patronymic = reg_info.split()

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
        if user[1]==id_telegram:
             return 0
    cursor.execute('INSERT INTO Users(id_telegram,second_name,first_name,patronymic,username) VALUES (?,?,?,?,?)',
                   (f'{id_telegram}',f'{second_name}',f'{first_name}',f'{patronymic}',f'{username}'))
    connection.commit()
    return 1

def data_base_reader_con1(id_telegram):
    connection = sqlite3.connect(r'Bot_Assist/Head/DataBase.db')
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
        if user[1]==id_telegram:
            return user[1]
    return 0

def data_base_reader_con2(di):
    connection = sqlite3.connect(r'Bot_Assist/Head/DataBase.db')
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

    cursor.execute('SELECT first_name,second_name FROM Users')
    users = cursor.fetchall()
    return users


names = [
    "Иванов Иван Иванович",
    "Петрова Анна Сергеевна",
    "Сидоров Дмитрий Олегович",
    "Кузнецова Екатерина Владимировна",
    "Смирнов Алексей Петрович",
    "Попова Ольга Николаевна",
    "Лебедев Михаил Александрович",
    "Козлова Мария Дмитриевна",
    "Новиков Сергей Игоревич",
    "Морозова Анастасия Андреевна",
    "Волков Андрей Викторович",
    "Соловьева Юлия Павловна",
    "Васильев Павел Евгеньевич",
    "Зайцева Елена Станиславовна",
    "Павлов Артем Константинович",
    "Семенова Ирина Васильевна",
    "Голубев Денис Юрьевич",
    "Виноградова Татьяна Олеговна",
    "Богданов Роман Артемович",
    "Воробьева Надежда Федоровна",
    "Федоров Григорий Степанович",
    "Михайлова Людмила Геннадьевна",
    "Беляев Виталий Романович",
    "Титова Ксения Валерьевна",
    "Комаров Станислав Борисович"
]
#id_telegram = 1
# for reg_info in names:
#     username = '4'
#print( data_base_reader(id_telegram))