from django.contrib.auth.hashers import make_password
import re


def validate_user(password, pwd, username, email):
    return (
        validate_password(password, pwd) and
        validate_username(username) and
        validate_email(email)
    )


def validate_password(password, pwd):
    return password == pwd and len(password) >= 8 and find_char(password)


# Verifica se tem letras e digitos na senha
def find_char(text):
    char = any(char.isalpha() for char in text)
    digit = any(char.isdigit() for char in text)
    return char and digit


def validate_username(username):
    return False if len(username) < 4 else True


def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[com]', email) is not None


def validate_question(question):
    if question and len(question) > 3:
        return True


def validate_answer(answer):
    if answer is not None and len(answer) > 3:
        return make_password(answer)


# Validate profile
def validate_profile(name, lastname, profession, telephone):
    return (
        validate_name(name) and
        validate_lastname(lastname) and
        validate_profession(profession) and
        validate_telephone(telephone)
    )


def validate_name(name):
    if name and len(name) > 2 and not any(char.isdigit() for char in name):
        return name.capitalize()


def validate_lastname(lastname):
    if lastname and not any(char.isdigit() for char in lastname):
        return lastname.capitalize()


def validate_profession(profession):
    if profession and len(profession) > 3:
        return profession.captalize()


def validate_telephone(telephone):
    digits_only = re.sub(r'\D', '', telephone)
    pattern = re.compile(r'^\(\d{2}\)\d{4,5}-\d{4}$')
    return bool(pattern.match(digits_only))
