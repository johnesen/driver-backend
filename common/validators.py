from common.exceptions import IncorrectPasswordException
from accounts.settings import PASSWORD_RE



def validate_user_password(password: str, conf_password: str) -> str:
    if not PASSWORD_RE.match(password):
        raise IncorrectPasswordException('Password min lenght is 8, and it must contains A-Z, a-z, 0-9')
    if password != conf_password:
        raise IncorrectPasswordException('Passwords must match')
    return password
