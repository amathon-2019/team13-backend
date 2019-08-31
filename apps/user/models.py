import binascii
import os
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .enums import DeviceType


class UserManager(BaseUserManager):
    def _create_user(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.pop('password')

        if username is None:
            raise ValueError(
                "아이디는 필수입니다."
            )

        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **kwargs):
        if password is None:
            raise ValueError(
                "관리자는 비밀번호가 필수입니다."
            )

        kwargs.update({
            'password': password,
            'is_admin': True,
        })

        return self._create_user(**kwargs)


class User(AbstractBaseUser):
    username = models.CharField(
        '아이디',
        max_length=50,
        unique=True
    )
    is_active = models.BooleanField(
        '활성화 여부',
        default=True
    )
    is_logged_in = models.BooleanField(
        '로그인 여부',
        default=False
    )
    is_admin = models.BooleanField(
        '관리자 여부',
        default=False
    )
    date_joined = models.DateTimeField(
        '가입일',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        '수정일',
        auto_now=True
    )

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '유저들'

    def __str__(self):
        return self.username

    def is_staff(self):
        return self.is_active and self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active and self.is_admin

    def has_perms(self, perm_list, obj=None):
        return self.is_active and self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin


def default_token_expire():
    now = datetime.now()
    return now + timedelta(days=30)  

class Token(models.Model):
    key = models.CharField(
        '키',
        max_length=40,
        primary_key=True
    )
    device = models.SmallIntegerField(
        '디바이스',
        choices=DeviceType.choices(),
        null=True,
        blank=True
    )
    user =models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='auth_token',
        on_delete=models.CASCADE,
        verbose_name='유저'
    )
    is_active = models.BooleanField(
        '활성화 여부',
        default=True
    )
    expired = models.DateTimeField(
        '만료일',
        default=default_token_expire
    )
    created = models.DateTimeField(
        '생성일',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        '수정일',
        auto_now=True
    )

    class Meta:
        db_table = 'token'
        verbose_name = '토큰'
        verbose_name_plural = '토큰 목록'

    def __str__(self):
        return self.key

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)
