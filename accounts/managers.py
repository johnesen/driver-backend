from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login, is_superuser, is_staff, is_active, password=None):
        if not login:
            raise ValueError("User must have a username")
        user = self.model(
            login=login,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, password=None):
        """
        create user
        """
        return self._create_user(
            login=login,
            is_superuser=False,
            is_staff=False,
            is_active=True,
            password=password,
        )

    def create_superuser(self, login, password):
        """
        superuser creation
        """
        return self._create_user(
            login=login,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            password=password,
        )
