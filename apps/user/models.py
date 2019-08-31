from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


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
