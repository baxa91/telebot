from django.db import models
from django.utils.translation import gettext_lazy as gtl
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(f'The given {settings.USERNAME_FIELD} must be set')
        extra_fields.update({
            settings.USERNAME_FIELD: username
        })
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, username_field, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        username_field = username_field.lower()
        return self.create_user(username_field, password, **extra_fields)

    def create_admin(self, username_field, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username_field, password, **extra_fields)

    def create_superuser(self, username_field, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username_field, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=70, unique=True, verbose_name=gtl('Username'))

    first_name = models.CharField(max_length=500, blank=True, null=True, verbose_name=gtl('First Name'))
    last_name = models.CharField(max_length=500, blank=True, null=True, verbose_name=gtl('Last Name'))
    middle_name = models.CharField(max_length=500, blank=True, null=True, verbose_name=gtl('Middle Name'))
    telegram_id = models.CharField(max_length=500, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=gtl('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=gtl('Updated At'))

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=gtl('Date of registration'))
    is_superuser = models.BooleanField(default=False, verbose_name=gtl('Is Superuser'))
    is_admin = models.BooleanField(default=False, verbose_name=gtl('Is Admin'))
    is_active = models.BooleanField(default=True, verbose_name=gtl('Is Active'))
    is_staff = models.BooleanField(default=False, verbose_name=gtl('Is Staff'))

    USERNAME_FIELD = 'username'

    objects = UserManager()

    @property
    def full_name(self):
        first_name = self.first_name if self.first_name else ''
        last_name = self.last_name if self.last_name else ''
        middle_name = self.middle_name if self.middle_name else ''
        full_name = f"{last_name} {first_name} {middle_name}".strip()
        return full_name if len(full_name) > 0 else gtl('Data not filled')

    def __str_gtl(self):
        return self.full_name

    class Meta:
        verbose_name = gtl('User')
        verbose_name_plural = gtl('Users')
