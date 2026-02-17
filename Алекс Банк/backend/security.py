# ПРОВЕРКА ДАННЫХ АККАУНТА

from datetime import datetime
import re
from typing import List, Tuple 


# класс всех проверок
class AllValidations:
    def __init__(self, number_phone, password, year_of_birth):
        self._number_phone = number_phone
        self._password = password
        self._year_of_birth = year_of_birth

        # объекты всех проверок
        self._age_validator = AgeVerification()
        self._phone_validator = NumberPhoneVerification()
        self._password_validator = PasswordVerification()


    # ищем все ошибки
    def all_validations(self):
        # ошибки возраста
        age_errors = self._age_validator.validation(self._year_of_birth)
        # ошибки номера телефона
        number_phone_errors = self._phone_validator.validation(self._number_phone)
        # ошибки пароля
        password_errors = self._password_validator.validation(self._password)

        # словарь ошибок
        errors = {
            'Возраст: ': age_errors,
            'Номер телефона: ': number_phone_errors,
            'Пароль: ': password_errors
        }
        
        # возвращаем словарь ошибок
        return errors



    # проверка возраста
class AgeVerification:
    
    MIN_AGE = 18
    MAX_AGE = 120
    # проходим по всем проверкам
    def validation(self, year_of_birth: str) -> List[str]:

        # список ошибок
        errors = []


        # храним все методы проверок ошибок
        validations = [self._year_is_num, 
                       self._age_over_18]


        # ищем ошибки
        for validation in validations:
            result, message = validation(year_of_birth)
            if not result:
                errors.append(message)


        # возвращаем ошибки
        return errors


    # проверка что год - число
    def _year_is_num(self, year_of_birth: str) -> Tuple[bool, str]:
        # Проверяем что строка состоит ТОЛЬКО из цифр
        if year_of_birth.strip().isdigit():
            return True, "Введено число"
        return False, "Год должен быть числом!"


    # проверка на возраст лет
    def _age_over_18(self, year_of_birth: str) -> Tuple[bool, str]:
        try:
            age = datetime.now().year - int(year_of_birth)
        except ValueError:
            return False, "Год должен быть числом!"
        if age < self.MIN_AGE:
            return False, f"Возраст должен быть от {self.MIN_AGE} лет!"
        elif age > self.MAX_AGE:
            return False, f"Возраст не может быть больше {self.MAX_AGE} лет!"
        elif age < 0:
            return False, "Год рождения не может быть в будущем!"
        
        return True, "Возраст подходит"

    


    # проверка номера телефона
class NumberPhoneVerification:

    LEN_NUMBER_PHONE_PLUS_7 = 12
    LEN_NUMBER_PHONE_8 = 11
    MIN_LEN_NUMBER_PHONE = 11

    # проходим по всем проверкам
    def validation(self, number_phone: str) -> List[str]:

        # список ошибок
        errors: List[str] = []

        # храним все методы проверок ошибок
        validations = [self._number_phone_len_check, 
                       self._checking_for_numbers]


        # ищем ошибки
        for validation in validations:
            result, message = validation(number_phone.replace(' ', ''))
            if not result:
                errors.append(message)

        # возвращаем ошибки
        return errors



    # проверка на длинну
    def _number_phone_len_check(self, number_phone: str) -> Tuple[bool, str]:
        # проверка минимальной длинны
        if len(number_phone) < self.MIN_LEN_NUMBER_PHONE:
            return False, "Номер слишком короткий"

        # если начиначется с +7
        if number_phone.startswith('+7') and len(number_phone) != self.LEN_NUMBER_PHONE_PLUS_7:
            return False, "Номер слишком короткий"

        # если начинатеся с 8
        elif number_phone.startswith('8') and len(number_phone) != self.LEN_NUMBER_PHONE_8:
            return False, "Номер слишком короткий"
        
        # проверка на первую цифру
        elif not (number_phone.startswith('8') or number_phone.startswith('+7')):
            return False, "Номер недействительный"

        return True, 'Длинна соответствует требованиям'


    # проврека на наличие букв и лишних символов
    def _checking_for_numbers(self, number_phone: str) -> Tuple[bool, str]:
        try:
            int(number_phone)
        except ValueError as e:
            return False, "В номере телефона не должно быть букв и лишних символов!"

        return True, "В номере нет букв и лишних символов"




# проверка пароля
class PasswordVerification:

    MIN_LEN_PASSWORD = 8
    DIGIT_PATTERN = r'[0-9]'
    UPPERCASE_PATTERN = r'[A-Z]'
    LOWERCASE_PATTERN = r'[a-z]'
    SYMBOL_PATTERN = r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]'

    # проходим по всем проверкам
    def validation(self, password: str) -> List[str]:
        
        # список ошибок
        errors: List[str] = []

        # храним все методы проверок ошибок
        validations = [self._has_no_spaces, 
                       self._check_len_password,
                       self._have_uppercase_letter,
                       self._have_lowercase_letter,
                       self._have_digit,
                       self._have_symbol]


        # ищем ошибки
        for validation in validations:
            result, message = validation(password)
            if not result:
                errors.append(message)


        # возвращаем ошибки
        return errors



    def _has_no_spaces(self, password: str) -> Tuple[bool, str]:
        if ' ' in password:
            return False, "Пароль не должен содержать пробелов"
        return True, "Пароль без пробелов"

            
    # проверка длинны пароля
    def _check_len_password(self, password: str) -> Tuple[bool, str]:

        if len(password) < self.MIN_LEN_PASSWORD:
            return False, f"Пароль должен содержать хотя бы {self.MIN_LEN_PASSWORD} символов!"
        return True, "Длина соответствует"


    # проверка на наличие заглавной буквы
    def _have_uppercase_letter(self, password: str) -> Tuple[bool, str]:



        if not re.search(self.UPPERCASE_PATTERN, password):            
            return False, "В пароле нет заглавной буквы!"
        return True, "В пароле есть заглавная буква"


    # проверка на наличие строчной буквы
    def _have_lowercase_letter(self, password: str) -> Tuple[bool, str]:

        if not re.search(self.LOWERCASE_PATTERN, password):
            return False, "В пароле нет строчной буквы!"
        return True, "В пароле есть строчная буква"


    # проверка на наличие цифры
    def _have_digit(self, password: str) -> Tuple[bool, str]:

        if not re.search(self.DIGIT_PATTERN, password):
            return False, "В пароле нет цифры!"
        return True, "В пароле есть цифра"


    # проверка на наличие символа   
    def _have_symbol(self, password: str) -> Tuple[bool, str]:

        if not re.search(self.SYMBOL_PATTERN, password):
            return False, "В пароле нет символа!"
        return True, "В пароле есть символ"






if __name__ == '__main__':
    # Тест отдельных валидаторов
    print("________ТЕСТ ОТДЕЛЬНЫХ ВАЛИДАТОРОВ________")
    chek_year_of_birth = AgeVerification()
    chek_number_phone = NumberPhoneVerification()
    chek_password = PasswordVerification()

    print("Возраст 2007:", chek_year_of_birth.validation('2007'))
    print("Номер +79111941032:", chek_number_phone.validation('+79111941032'))
    print("Пароль 'Sasha_19042007':", chek_password.validation('Sasha_19042007'))
    
    print("\n" + "-"*50 + "\n")
    
    # Тест общего класса
    print("________ТЕСТ ОБЩЕГО КЛАССА AllValidations________")
    
    # Тест 1: Все данные корректные
    print("\nТест 1 - Корректные данные:")
    validator1 = AllValidations(
        number_phone='+79111941032',
        password='Sasha_19042007',
        year_of_birth='1990'
    )
    results1 = validator1.all_validations()
    for field, errors in results1.items():
        print(f"{field} {errors if errors else ['✓ Все хорошо']}")
    
    # Тест 2: Данные с ошибками
    print("\nТест 2 - Данные с ошибками:")
    validator2 = AllValidations(
        number_phone='123',             # Неправильный номер
        password='weak',                # Слабый пароль
        year_of_birth='2010'            # Меньше 18 лет
    )
    results2 = validator2.all_validations()
    for field, errors in results2.items():
        print(f"\n{field}")
        if errors:
            for error in errors:
                print(f"  ✗ {error}")
        else:
            print("  ✓ Все хорошо")
