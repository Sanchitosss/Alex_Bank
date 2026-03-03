# ЗАПРОСЫ К БАЗЕ ДАННЫХ


# Создание таблицы
CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                surname TEXT NOT NULL,
                year_of_birth INTEGER NOT NULL,
                number_phone TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                balance FLOAT DEFAULT 0
                )'''


# Регистрация
REGISTRATION = "INSERT INTO users (first_name, surname, age, number_phone, password) VALUES (?, ?, ?, ?, ?)"


# изменение номера телефона
UPDATE_NUMBER_PHONE = '''UPDATE users SET number_phone = ?
                        WHERE number_phone = ?'''


# проверка на наличие пользователя
USER_PRESENCE = '''SELECT * FROM users
                    WHERE number_phone = ? AND password = ?'''
