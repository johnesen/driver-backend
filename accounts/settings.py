import re
from config.settings.env import env


PHONE_RE = re.compile(r"\+996\d{9}\b")
MAIL_RE = re.compile(r"\b[\w.-]+@[\w.-]+.\w{2,4}\b")
PASSWORD_RE = re.compile(r"[\w.-]{8,}")


class UserTypes:
    driver = "driver"
    client = "client"

    @classmethod
    def choices(cls):
        return (
            (cls.driver, cls.driver),
            (cls.client, cls.client),
        )
