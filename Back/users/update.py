from .validate import *


def update_user(user, username, email, password, pwd, question, answer):
    if validate_username(username):
        user.username = username
    if validate_email(email):
        user.email = email
    if validate_question(question):
        user.recovery.question = question
    if answer:
        new_answer = validate_answer(answer)
        if new_answer:
            user.recovery.answer = new_answer

    if password == pwd and password and pwd:
        if validate_password(password, pwd):
            user.set_password(password)

    user.save()
    user.profile.save()


def update_profile(profile, name, lastname, area, profession, telephone, description, active):
    pass
