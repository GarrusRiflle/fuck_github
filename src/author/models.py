from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password, email):
        u = User()
        u.username = username
        u.email = self.normalize_email(email)
        u.set_password(password)
        u.save(using=self._db)
        return u
    def create_superuser(self, username, email, password):
        u = User()
        u.username = username
        u.email = self.normalize_email(email)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.is_admin = True
        u.save(using=self._db)
        return u

class User(AbstractUser):
    class Meta:
        db_table = 'author_user'
    avatar = models.ImageField(upload_to='photo/', blank=True, null=True, default='photo/empty.png')
    rating = models.IntegerField(default=0, null=True)
    objects = UserManager()