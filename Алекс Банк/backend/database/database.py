import sqlite3
from database.queries import * # файл с запросами к бд


class DataBase:

    # передаём название файла бд
    def __init__(self, file_db):
        self.file_db = file_db
        self._create_table()

    # создание базы данных
    def _create_table(self):
        """Создаёт таблицу, если её нет"""
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(CREATE_TABLE)
                print("Таблица users создана или уже существует")
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
                
        # ошибка подключения
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")


    # проверка на наличие пользователя
    def user_presence(self, number_phone, password):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(USER_PRESENCE, (number_phone, password))
                data_user = cursor.fetchone()
                if data_user:
                    return True, "Пользователь найден", data_user
                return False, "Пользователь не найден", None

        # ошибка подключения
        except sqlite3.OperationalError as e:
            return False, "Ошибка подклыючения к базе данных!", None


    # добавление аккаунта
    def registration(self, first_name, surname, year_of_birth, number_phone, password):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                print(f"Пытаюсь вставить: {first_name}, {surname}, {year_of_birth}, {number_phone}")
                cursor.execute(REGISTRATION, (first_name, surname, year_of_birth, number_phone, password))
                
                print("Ищу пользователя по номеру:", number_phone)
                cursor.execute(USER_PRESENCE, (number_phone, password))
                data_user = cursor.fetchone()
                print(f"Найден пользователь: {data_user}")
                return True, "Регистрация выполнена!", data_user

        # ошибка подключения
        except sqlite3.OperationalError as e:
            return False, "Ошибка подключения к базе данных!", None

        # используется уже существующий номер телефона
        except sqlite3.IntegrityError as e:
            return False, "Этот номер телефона уже зарегистрирован!", None


    # изменение номера телефона
    def update_number_phone(self, number_phone, new_number_phone):
        try:
            with sqlite3.connect(self.file_db) as conn:
                cursor = conn.cursor()
                cursor.execute(UPDATE_NUMBER_PHONE, (new_number_phone, number_phone))
                return True, "Номер телефона успешно изменён!"

        # ошибка подключения
        except sqlite3.OperationalError as e:
            return False, "Ошибка подключения к базе данных!"

        # используется уже существующий номер телефона
        except sqlite3.IntegrityError as e:
            return False, "Номер телефона уже занят!"
