# ЗАПРОСЫ К БАЗЕ ДАННЫХ


# Создание таблицы
CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                age INTEGER NOT NULL,
                number_phone TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
                )'''


# Регистрация
REGISTRATION = "INSERT INTO users (first_name, surname, number_phone, password, replay_password) VALUES (?, ?, ?, ?, ?)"


# Вход
ENTRANCE = '''SELECT number_phone, password FROM users
                WHERE number_phone = ? AND password = ?'''


# изменение имени
UPDATE_USERNAME = '''UPDATE users SET username = ?
                    WHERE number_phone = ?''' 


# изменение номера телефона
UPDATE_NUMBER_PHONE = '''UPDATE users SET number_phone = ?
                        WHERE number_phone = ?'''





# проверка на наличие пользователя
USER_PRESENCE = '''SELECT number_phone, password FROM users
                    WHERE number_phone = ? AND password = ?'''