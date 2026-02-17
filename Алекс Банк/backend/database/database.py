import sqlite3
from database.queries import * # файл с запросами к бд


class DataBase:

    # передаём название файла бд
    def __init__(self, file_db):
        self.file_db = file_db

    # проверка на наличие пользователя
    def user_presence(self, number_phone, password):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(USER_PRESENCE, (number_phone, password))
                user = cursor.fetchone()
                if user:
                    return True, "Пользователь найден"
                return False, "Пользователь не найден"
        except sqlite3.OperationalError as e:
            return False, "Ошибка подклыючения к базе данных!"


    # добавление аккаунта
    def addition(self, first_name, surname, number_phone, password, replay_password):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(REGISTRATION, (first_name, surname, number_phone, password, replay_password))
                return True, "Регистрация выполнена!"

        # ошибка подключения
        except sqlite3.OperationalError as e:
            return False, "Ошибка подклыючения к базе данных!"

        # используется уже существующий номер телефона
        except sqlite3.IntegrityError as e:
            return False, "Номер телефона уже занят!"


    # вход в аккаунт
    def entrance(self, number_phone, password):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(ENTRANCE, (number_phone, password))
                return True, "Успешный вход!"

        # ошибка подключения
        except sqlite3.OperationalError as e:
            return None, "Ошибка подключения к базе данных!"

    # изменение имени пользователя
    def update_username(self, number_phone, new_name):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(UPDATE_USERNAME, (new_name, number_phone))
                return True, "Имя успешно изменено!"

        # ошибка подключения
        except sqlite3.OperationalError as e:
            return None, "Ошибка подключения к базе данных!"

    # изменение номера телефона
    def update_number_phone(self, number_phone, new_number_phone):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(UPDATE_NUMBER_PHONE, (new_number_phone, number_phone))
                return True, "Номер телефона успешно изменён!"

        # ошибка подключения
        except sqlite3.OperationalError as e:
            return None, "Ошибка подключения к базе данных!"

        # используется уже существующий номер телефона
        except sqlite3.IntegrityError as e:
            return None, "Номер телефона уже занят!"