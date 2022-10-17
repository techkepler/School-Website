from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

# Creating a Custom User Model
class UserManager(BaseUserManager):
    def create_user(self, uid, role, password=None, password2=None, **other_fields):
        if not uid:
            raise ValueError("User must have an id.")
        user = self.model(uid=uid, role=role, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, role, password=None, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_admin", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_admin") is not True:
            raise ValueError("Superuser must be assigned to is_admin=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        user = self.create_user(uid, role, password, **other_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "uid"
    REQUIRED_FIELDS = ["role"]

    objects = UserManager()

    def __str__(self):
        return self.uid
