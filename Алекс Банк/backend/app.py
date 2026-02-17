from flask import Flask, render_template, url_for, request, flash
from database.database import DataBase # работа с бд
from security import AllValidations


app = Flask(__name__, template_folder='../frontend/templates',
                        static_folder='../frontend/static')

# объект на основе клааса для работы с бд
db = DataBase('training.db')


# главная страница
@app.route('/')
def index():
    return render_template('index.html')


# вход в аккаунт
@app.route('/authentication', methods=['POST', 'GET'])
def auth():
    
    # если нажимается кнопка 'войти'
    if request.method == 'POST':
        number_phone = request.form.get('number_phone', '').strip()
        password = request.form.get('password', '').strip()
        
        # если хотя бы одно поле пустое
        if not number_phone or not password:
            flash('Все поля должны быть заполнены!')
            return render_template('authentication.html')
        
        # результат и сообщение из функции, которая проверяет в бд наличие пользователя
        success, message = db.user_presence(number_phone, password)

        # если пользователь найден
        if success:
            return render_template('account.html') # сделать переход в аккаунт!!!!!!!
        # если пользователь не найден
        else:
            flash(message)
            return render_template('authentication.html')
    
    # при переходе на эту страницу
    return render_template('authentication.html')



# регистрация аккаунта
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
        replay_password = request.form.get('replay_password', '').strip()


        # если хотя бы одно поле не заполнено
        fields = [first_name, surname, number_phone, password, replay_password]
        if not all(fields):
            flash('Все поля должны быть заполнены!')
            return render_template('registration.html')


        # проверка совпадения паролей
        if password != replay_password:
            flash('Пароли не совпадают!')
            return render_template('registration.html')
        
        # экземпляр класса, проверяющего все ошибки
        valids = AllValidations(number_phone=number_phone, password=password, year_of_birth=year_of_birth)
        
        # ошибки введённых данных
        errors = valids.all_validations()

        # ищем ошибки в ведённых данных
        has_errors = False
        for key, error in errors.items():
            if error:
                has_errors = True
        # если есть хотя бы одна ошибка
        if has_errors:
            for field_name, error_list in errors.items():
                for error in error_list:
                    flash(f'{field_name}: {error}')
            
            return render_template('registration.html')

        # добавляем пользователя в бд, если проверки пройдены
        # ДОБАВИТЬ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # при переходе на эту страницу
    return render_template('registration.html')





if __name__ == '__main__':
    app.run(debug=True)