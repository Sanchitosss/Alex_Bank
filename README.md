Bank App

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![Validation](https://img.shields.io/badge/Validation-✅-green)

Банковское приложение на Flask с полноценной валидацией данных.

# 🚀 Стек технологий
Backend: Python, Flask

База данных: SQLite

Frontend: HTML

Безопасность: Сессии, валидация всех полей

# ✅ Реализовано
🔐 Регистрация и вход с проверкой данных

📱 Валидация номера телефона (Российские номера, +7/8)

🔑 Валидация пароля (8+ символов, цифры, буквы, спецсимволы)

📅 Проверка возраста (18+ лет)

👤 Личный кабинет с отображением данных

🚪 Выход из аккаунт

💾 Работа с БД (SQLite, параметризованные запросы)

🧪 Самопроверка в каждом модуле


Алекс Банк/

├── backend/

│   ├── app.py              # Основной файл приложения

│   └── security.py          # Валидация данных

├── database/

│   ├── database.py          # Класс для работы с БД

│   └── queries.py           # SQL запросы

├── frontend/

│   ├── templates/           # HTML шаблоны

│   └── static/              # CSS, JS (в будущем)

└── requirements.txt         # Зависимости



🛠️ Установка и запуск
bash
# Клонировать репозиторий
git clone https://github.com/username/bank-app.git

# Перейти в папку проекта
cd bank-app

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
python backend/app.py




# 🎯 В планах
🔄 PostgreSQL вместо SQLite

📦 SQLAlchemy ORM

🧪 Тесты (pytest)

💰 Пополнение баланса

📊 История операций

🎨 Красивый фронтенд (CSS)


📝 О проекте

Проект создан в учебных целях для демонстрации навыков backend-разработки на Python. В коде сделан акцент на безопасность, валидацию данных и чистую архитектуру.
