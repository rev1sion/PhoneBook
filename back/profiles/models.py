from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    BaseUserManager,
    AbstractBaseUser,
    Permission,
    Group
)
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.dispatch import receiver

import uuid

from back.permissions.choices import *


def get_default_uuid():
    return uuid.uuid4().hex


class UserManager(BaseUserManager):
    def create_user(self,
                    position,
                    email,
                    birthday,
                    full_name,
                    avatar,
                    bio,
                    accepted_tos=None,
                    is_active=True,
                    password=None
                    ):
        if not accepted_tos:
            raise ValueError(_("Пользователи должны принять соглашение  "))

        user = self.model(
            email=self.normalize_email(email),
            position=position,
            avatar=avatar,
            birthday=birthday,
            full_name=full_name,
            bio=bio,
            accepted_tos=True,
            is_active=is_active
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,
                         email,
                         # birthday,
                         password,
                         # position,
                         full_name,
                         # bio,
                         ):
        user = self.create_user(
            email,
            # position,
            full_name,
            # birthday,
            # bio,
            accepted_tos=True,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        # try:
        #     admins = Group.objects.get(name__iexact="Администраторы")
        # except Group.DoesNotExist:
        #     admins = Group.objects.create(name="Администраторы")
        # admins.permissions.add(
        #     Permission.objects.get(ADMINS_PERMISSIONS))
        # user.groups.add(admins)
        user.save()
        return user

    def create_employee(self, email, birthday, password, position, full_name, bio,):
        user = self.create_user(
            email,
            birthday,
            password,
            position,
            full_name,
            bio,
            accepted_tos=True,
            password=password,
        )
        try:
            employee = Group.objects.get(name__iexact="Сотрудники")
        except Group.DoesNotExist:
            employee = Group.objects.create(name="Сотрудники")

        employee.permissions.add(
            Permission.objects.get(MEMBERS_PERMISSIONS))  # add can_give_discount permission
        user.groups.add(employee)
        user.save()
        return user


DEFAULT_IMAGE = 'static/media/default.jpg'


class User(AbstractBaseUser, PermissionsMixin):
    # phone = models.ForeignKey(PhoneNumber, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=122, null=True, blank=True, verbose_name=_("Должность"))
    uuid = models.CharField(_("UUID"), max_length=32, editable=False, null=False,
                            blank=False, unique=True, default=get_default_uuid)
    email = models.EmailField(_("Имейл"), max_length=125, unique=True)
    full_name = models.CharField(_("Ф.И.О."), max_length=120)
    avatar = models.ImageField(_("Изображение"), upload_to='avatars/', default=DEFAULT_IMAGE, null=True, blank=True)
    bio = models.TextField(_("О пользователе"), max_length=300, null=True, blank=True)
    birthday = models.DateField(_("День рождения"), null=True, blank=True)
    accepted_tos = models.BooleanField(default=True, verbose_name=_("Принято соглашение"))
    is_active = models.BooleanField(_("Активен"), default=True)
    is_admin = models.BooleanField(_("Админ"), default=False)
    created_at = models.DateTimeField(_("Создан"), auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(_("Обновлен"), auto_now_add=False, auto_now=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return "%s. %s" % (self.id, self.full_name)

    class Meta:
        ordering = ["full_name"]
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    def is_staff(self):
        return self.is_admin

    def image_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return DEFAULT_IMAGE
    # def set_image_to_default(self):
    #     self.image.delete(save=False)  # delete old image file
    #     self.image = DEFAULT_IMAGE
    #     self.save()

    def get_short_name(self):
        l = self.full_name.split(' ')[1:2]
        name = ''.join(l)
        return name


class PhoneNumber(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Пользователь"))
    phone_mobile = models.CharField(_("Мобильный тел."), max_length=26, null=True, blank=True)
    phone_small = models.PositiveSmallIntegerField(_("Короткий номер"), null=True, blank=True)
    phone_city = models.PositiveIntegerField(_("Городской номер"), null=True, blank=True)

    def __str__(self):
        return "%s, %s" % (self.phone_city, self.phone_small)

    class Meta:
        verbose_name = _("Номер телефона")
        verbose_name_plural = _("Номера телефонов")