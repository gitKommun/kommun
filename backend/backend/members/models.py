import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from communities.models import Community
from django.contrib.contenttypes.models import ContentType

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio para crear un usuario')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Eliminar el campo de nombre de usuario
    
    #Personal data
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=30)
    surnames = models.CharField(_('surnames'), max_length=120)
    birthdate = models.DateField(verbose_name=_("Birthdate"), null=True, blank=True)
    address = models.CharField(_('postal address'), max_length=255)
    phone_number = models.CharField(_('phone number'), max_length=20, null=True, blank=True)
    personal_id_number = models.CharField(_('user ID'), max_length=20, null=True, blank=True)  # DNI, NIE, or passport
    personal_id_type = models.CharField(_('document type'), null=True, blank=True, max_length=20, choices=[('DNI', 'DNI'), ('NIE', 'NIE'), ('PASSPORT', 'Passport')])

    #Configuration and usage
    current_community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True)
    language_config = models.CharField(_('language configuration'), null=True, blank=True, max_length=2, choices=[('EN', 'English'), ('ES', 'Spanish')])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.name} {self.surnames}"


