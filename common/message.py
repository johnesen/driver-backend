def my_message(code, for_reset=False):
    """
        Message to user email
    """
    body = "Ваш код активации: " + code
    subject = "Активация аккаунта"
    if for_reset:
        body = "Ваш код для сброса пароля: " + code
        subject = "Сброс пароля"

    message = {"body": body, "subject": subject}
    return message
