from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from communities.models import Community, Property
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
    username = None  # Eliminar el campo de nombre de usuario
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=30)
    surnames = models.CharField(_('surnames'), max_length=150)
    birthdate = models.DateField(verbose_name=_("Birthdate"), null=True, blank=True)
    addressLetters = models.CharField(_('postal address'), max_length=255)
    phoneNumber = models.CharField(_('phone number'), max_length=20, null=True, blank=True)

    bankAccount = models.CharField(_('bank account'), max_length=22, null=True, blank=True) #IBAN
    languageConf = models.CharField(_('language configuration'), null=True, blank=True, max_length=2, choices=[('EN', 'English'), ('ES', 'Spanish')])
    documentID = models.CharField(_('user ID'), max_length=20, null=True, blank=True)  # DNI, NIE, or passport
    documentType = models.CharField(_('document type'), null=True, blank=True, max_length=20, choices=[('DNI', 'DNI'), ('NIE', 'NIE'), ('PASSPORT', 'Passport')])
    contactIsPublic = models.BooleanField(_('public contact'), default=False, null=True, blank=True)

    current_community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.name} {self.surnames}"



#class Owner which is an extenion of User
class Owner(User):
    properties = models.ManyToManyField(Property, verbose_name="Properties", related_name="owners", blank=True) #privado
    hasPendingPayment = models.BooleanField(null=True, blank=True) #privado

    class Meta:
        verbose_name = _("Owner")
        verbose_name_plural = _("Owners")

    def add_property(self, property):
        self.properties.add(property)

    def remove_property(self, property):
        self.properties.remove(property)

    def get_associated_community(self):
        # Primero, verifica si el Owner es el mainContact de alguna comunidad
        owner_type = ContentType.objects.get_for_model(self)
        communities_as_main_contact = Community.objects.filter(main_contact_type=owner_type, main_contact_id=self.id)
        if communities_as_main_contact.exists():
            return communities_as_main_contact.first()

        # Si no es el mainContact, busca la comunidad a través de las propiedades
        if self.properties.exists():
            # Asumiendo que cada propietario solo está asociado a una comunidad a través de sus propiedades
            return self.properties.first().community

        # Retorna None si no se encuentra ninguna asociación
        return None


class Administrator(User):
    companyName = models.CharField(_('company name'), max_length=20, unique=False, null=True, blank=True) 
    numCollegiate = models.CharField(_('number collegiate'), max_length=50, unique=True, null=True, blank=True)  

    class Meta:
        verbose_name = _("Administrator")
        verbose_name_plural = _("Administrators")


class Tenant(User):
    properties = models.ManyToManyField(Property, verbose_name="Properties", related_name="tenants", blank=True)

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")


    def add_property(self, property):
        self.properties.add(property)

    def remove_property(self, property):
        self.properties.remove(property)
