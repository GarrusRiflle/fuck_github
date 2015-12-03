from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password, email):
        u = User()
        u.username = username
        u.email = self.normalize_email(email)
        u.set_password(password)
        u.save()
        return u
    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    class Meta:
        db_table = 'author_user'
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    objects = UserManager()