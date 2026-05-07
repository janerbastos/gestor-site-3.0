from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings



class UserManager(BaseUserManager):

    """
    Gerenciador personalizado para o modelo User.

    Métodos:
        create_user(email, password=None, **extra_fields):
            Cria e salva um usuário com o e-mail e senha fornecidos.
            - email: E-mail do usuário (obrigatório).
            - password: Senha do usuário (opcional).
            - extra_fields: Campos adicionais para o usuário.
            Lança ValueError se o e-mail não for fornecido.

        create_superuser(email, password=None, **extra_fields):
            Cria e salva um superusuário com o e-mail e senha fornecidos.
            Define automaticamente os campos 'is_staff' e 'is_superuser' como True.
            - email: E-mail do superusuário.
            - password: Senha do superusuário.
            - extra_fields: Campos adicionais para o superusuário.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    """
    Modelo customizado de usuário para autenticação baseada em e-mail.

    Campos:
        email (EmailField): E-mail único do usuário, utilizado como identificador principal.
        is_active (BooleanField): Indica se a conta está ativa.
        is_staff (BooleanField): Indica se o usuário tem permissão de acesso ao admin.
        is_verified (BooleanField): Indica se o e-mail do usuário foi verificado.
        date_joined (DateTimeField): Data de criação da conta.

    Configurações:
        USERNAME_FIELD: Define o campo utilizado para login (e-mail).
        REQUIRED_FIELDS: Lista de campos obrigatórios além do e-mail e senha (vazia).

    Gerenciador:
        objects: Usa o UserManager personalizado para criação de usuários e superusuários.

    Métodos:
        __str__(): Retorna o e-mail do usuário como representação textual.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    @property
    def is_admin(self):
        return self.is_superuser or self.groups.filter(name='admin').exists()
    

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
