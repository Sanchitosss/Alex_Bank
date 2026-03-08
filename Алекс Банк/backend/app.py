from flask import Flask, render_template, redirect, url_for, request, flash, session
from database.database import DataBase # работа с бд
from security import AllValidations # проверка данных пользователя для регистрации
import bcrypt # хэширование паролей


app = Flask(__name__, template_folder='../frontend/templates',
                        static_folder='../frontend/static')

app.secret_key = 'sanechek_brat_001'

# объект на основе клааса для работы с бд
db = DataBase(r"C:\Users\5009044\OneDrive\Рабочий стол\Алекс Банк\backend\database\Alex_Bank.db")


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Вход в аккаунт
@app.route('/authentication', methods=['POST', 'GET'])
def authentication():
    
    # если нажимается кнопка 'войти'
    if request.method == 'POST':
        number_phone = request.form.get('number_phone', '').strip()
        password = request.form.get('password', '').strip()
        
        # если хотя бы одно поле пустое
        if not number_phone or not password:
            flash('Все поля должны быть заполнены!')
            return render_template('authentication.html')
        
        # результат и сообщение из функции, которая проверяет в бд наличие пользователя
        success, message, data_user = db.user_presence(number_phone)

        # проверка на совпадение пароля
        if not data_user or not bcrypt.checkpw(password.encode('utf-8'), data_user[5]):
            flash('Неверный логин или пароль!')
            return render_template('authentication.html')

        # создаём сессию
        session['id'] = data_user[0]
        session['first_name'] = data_user[1]
        session['surname'] = data_user[2]
        session['year_of_birth'] = data_user[3]
        session['number_phone'] = data_user[4]
        session['balance'] = data_user[6]

        return redirect(url_for('account'))
    
    # при переходе на эту страницу
    return render_template('authentication.html')



# Регистрация аккаунта
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        # имя
        first_name = request.form.get('first_name', '').strip()
        # фамилия
        surname = request.form.get('surname', '').strip()
        # год рождения
        year_of_birth = request.form.get('year_of_birth', '').strip()
        # номер телефона
        number_phone = request.form.get('number_phone', '').strip()
        # пароль
        password = request.form.get('password', '').strip()
        # повтор пароля
        repeat_password = request.form.get('repeat_password', '').strip()


        # если хотя бы одно поле не заполнено
        fields = [first_name, surname, year_of_birth, number_phone, password, repeat_password]
        if not all(fields):
            flash('Все поля должны быть заполнены!')
            return render_template('registration.html')

        # проверка совпадения паролей
        if password != repeat_password:
            flash('Пароли не совпадают!')
            return render_template('registration.html')
        
        # экземпляр класса, проверяющего все ошибки
        valids = AllValidations(number_phone=number_phone, password=password, year_of_birth=year_of_birth)
        
        # ошибки введённых данных
        errors = valids.all_validations()

        # ищем ошибки в ведённых данных
        has_errors = any(error_list for error_list in errors.values())

        # если есть хотя бы одна ошибка
        if has_errors:
            for field_name, error_list in errors.items():
                # выводим ошибки
                for error in error_list:
                    flash(f'{field_name}: {error}')
            return render_template('registration.html')

        # проверка, что нет пользователя с таким номером
        success, message, data_user = db.user_presence(number_phone)
        if data_user:
            flash('Пользователь с таким номером уже существует!')
            return render_template('registration.html')

        # соль для хэширования
        salt = bcrypt.gensalt(rounds=12)
        
        # хэширование пароля
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # результаты и сообщение регистрации пользователя
        success, message, data_user = db.registration(first_name=first_name, surname=surname, year_of_birth=year_of_birth, number_phone=number_phone, password=hashed_password)
        
        # если успешно зарегистрировались
        if success:
            # создаём сессию
            session['id'] = data_user[0] # id
            session['first_name'] = data_user[1] # имя 
            session['surname'] = data_user[2] # фамилия
            session['year_of_birth'] = data_user[3] # год рождения
            session['number_phone'] = data_user[4] # номер телефона
            session['balance'] = data_user[6] # баланс
            
            return redirect(url_for('account'))

        # если ошибка добавления в бд
        else:
            flash(message)
            return render_template('registration.html')
        
    # при переходе на эту страницу
    return render_template('registration.html')


# Аккаунт
@app.route('/account', methods=['GET'])
def account():
    # если нет сессии - переходим на главную
    if 'id' not in session:
        return redirect(url_for('index'))
    
    # если есть сессия - переходим в аккаунт
    return render_template('account.html',
                          first_name=session['first_name'], # имя
                          surname=session['surname'], # фамилия
                          number_phone=session['number_phone'], # номер телефона
                          balance=session['balance']) # баланс


# Удаление аккаунта
@app.route('/delete', methods=['POST'])
def delete():
    # если нет сессии
    if 'id' not in session:
        return redirect(url_for('index'))

    # удаляем аккаунт
    success, message = db.delete_user(session['number_phone'])

    # если аккаунт удалился
    if success:
        session.clear()  # очищаем сессию здесь!
        return redirect(url_for('index'))

    # если аккаунт не удалился
    return redirect(url_for('account'))


# Выход из аккаунта
@app.route('/logout', methods=['POST'])
def logout():
    session.clear() # Удаляем все данные сессии
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)
