from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, nickname, password=None, **extra_fields):
        if not username:
            raise ValueError('회원가입을 위해서 유저이름이 필요합니다.')
        if not nickname:
            raise ValueError('회원가입을 위해서 닉네임이 필요합니다.')

        extra_fields.setdefault('roles', [{'role': 'USER'}])
        
        user = self.model(
            username=username,
            nickname=nickname,
            **extra_fields
        )

        if extra_fields.get('roles')[0]['role'] == 'ADMIN': 
            user.is_staff = True
            user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, password=None, **extra_fields):
        extra_fields['roles'] = [{'role': 'ADMIN'}]
        return self.create_user(username, nickname, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('USER', '일반 사용자'),
        ('ADMIN', '관리자'),
    ]
    
    username = models.CharField(
        max_length=50, 
        unique=True, 
        validators=[MinLengthValidator(5, message='유저이름은 최소 5자 이상이어야 합니다.')]
    )
    nickname = models.CharField(
        max_length=30, 
        unique=True, 
        validators=[MinLengthValidator(5, message='닉네임은 최소 5자 이상이어야 합니다.')]
    )
    roles = models.JSONField(default=list)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname