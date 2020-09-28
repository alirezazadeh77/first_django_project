from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from product.validators import clean_phone_number_validator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, Phone_number, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not Phone_number:
            raise ValueError('The given Phone_number must be set')
        Phone_number = self.model.normalize_username(Phone_number)
        user = self.model(Phone_number=Phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, Phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(Phone_number, password, **extra_fields)

    def create_superuser(self, Phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(Phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    Phone_number = models.BigIntegerField(_("Phone number"), unique=True, validators=[clean_phone_number_validator, ])
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'Phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return str(self.Phone_number)
