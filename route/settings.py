class ContactTypes:
    email = "E-mail"
    phone = "phone number"
    telegram = "telegram"
    whatsapp = "whatsapp"

    @classmethod
    def choice(cls):
        return (
            (cls.email, cls.email),
            (cls.phone, cls.phone),
            (cls.telegram, cls.telegram),
            (cls.whatsapp, cls.whatsapp),
        )   
