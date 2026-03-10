# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
from flask import Flask, session
from database.database import DataBase
from security import NumberPhoneVerification

# дествия пользователя в аккаунте
class User:
    def __init__(self, data_user=None):
        if data_user:
            self._id = data_user[0] # id
            self._first_name = data_user[1] # имя
            self._surname = data_user[2] # фамилия
            self._year_of_birth = data_user[3] # год рождения
            self._number_phone = data_user[4] # номер телефона
            self._balance = data_user[6] # баланс


    # создание сессии
    def create_session(self):
        # создаём сессию
        session['id'] = self._id # id
        session['first_name'] = self._first_name # имя 
        session['surname'] = self._surname # фамилия
        session['year_of_birth'] = self._year_of_birth # год рождения
        session['number_phone'] = self._number_phone # номер телефона
        session['balance'] = self._balance # баланс


    # изменение номера телефона
    def update_number_phone(self, db, new_number_phone):
        # если новый номер совпадает со старым
        if session['number_phone'] == new_number_phone:
            return False, 'Новый номер телефона не должен совпадать с нынешним!'

        # проверка валидности нового номера телефона
        valid_number = NumberPhoneVerification()
        errors = valid_number.validation(new_number_phone)

        # если есть ошибки выводим их
        if errors:
            return False, 'Невалидный номер телефона'

        # если в номере нет ошибок, то изменяем его
        success, message = db.update_number_phone(session['number_phone'], new_number_phone)

        # если номер изменился
        if success:
            session['number_phone'] = new_number_phone # изменяем номер в сессии
            self._number_phone = new_number_phone # изменяем номер в атрибуте класса
            return True, message

        # если ошибка
        return False, message


    # удаление аккаунта
    def delete_account(self, db):
        success, message = db.delete_user(session['number_phone'])

        # если аккаунт удалился
        if success:
            session.clear() # очищаем сессию
            return True, message

        # если не удалился
        return False, message




if __name__ == '__main__':
    from flask import Flask, session
    
    app = Flask(__name__)
    app.secret_key = 'test_key'
    
    print('ТЕСТИРОВАНИЕ КЛАССА USER')
    print('-' * 40)
    
    # Тест 1: инициализация
    print('\n -------------- Проверка инициализации --------------')
    test_data = [1, 'Иван', 'Иванов', 1990, '+79991112233', 'hash', 1000]
    user = User(test_data)
    
    if user._id == 1:
        print('   ✅ id совпадает')
    if user._first_name == 'Иван':
        print('   ✅ имя совпадает')
    if user._surname == 'Иванов':
        print('   ✅ фамилия совпадает')
    if user._year_of_birth == 1990:
        print('   ✅ год рождения совпадает')
    if user._number_phone == '+79991112233':
        print('   ✅ телефон совпадает')
    if user._balance == 1000:
        print('   ✅ баланс совпадает')
    
    # Тест 2: создание сессии
    print('\n ---------------- Проверка создания сессии ----------------')
    
    with app.test_request_context():
        session.clear()
        user.create_session()
        
        if session.get('id') == 1:
            print('   ✅ id в сессии')
        if session.get('first_name') == 'Иван':
            print('   ✅ имя в сессии')
        if session.get('surname') == 'Иванов':
            print('   ✅ фамилия в сессии')
        if session.get('year_of_birth') == 1990:
            print('   ✅ год рождения в сессии')
        if session.get('number_phone') == '+79991112233':
            print('   ✅ телефон в сессии')
        if session.get('balance') == 1000:
            print('   ✅ баланс в сессии')
    
    # Тест 3: смена номера
    print('\n ---------------- Проверка смены номера ----------------')
    
    class MockDB:
        def update_number_phone(self, old, new):
            print(f'      БД: {old} -> {new}')
            return True, 'ok'
    

    with app.test_request_context():
        session.clear()
        user.create_session()
        print('      Сессия создана')
        
        # тот же номер
        success, msg = user.update_number_phone(MockDB(), '+79991112233')
        if not success:
            print('   ✅ защита от повторов работает')
        else:
            print('   ❌ защита не сработала')
        
        # новый номер
        success, msg = user.update_number_phone(MockDB(), '+79998887766')
        if success and session.get('number_phone') == '+79998887766':
            print('   ✅ номер меняется и сессия обновляется')
        else:
            print('   ❌ номер не меняется')
        
        # невалидный номер
        success, msg = user.update_number_phone(MockDB(), '89998887766')
        if not success:
            print('   ✅ валидация работает')
        else:
            print('   ❌ валидация пропустила плохой номер')
    
    # Тест 4: удаление
    print('\n ---------------- Проверка удаления ----------------')
    
    class MockDBDelete:
        def delete_user(self, phone):
            print(f'      БД: удаляем {phone}')
            return True, 'deleted'
    
    with app.test_request_context():
        # опять создаём сессию перед тестом
        session.clear()
        user.create_session()
        print('      Сессия создана')
        
        success, msg = user.delete_account(MockDBDelete())
        if success and len(session) == 0:
            print('   ✅ аккаунт удалён, сессия пустая')
        else:
            print('   ❌ ошибка при удалении')
    
    print('\n' + '-' * 40)
    print('Тесты закончены')






