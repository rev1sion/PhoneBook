import uuid
import re
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from back.profiles.models import User, PhoneNumber


class Organization(models.Model):
    name = models.CharField(_("Имя"), max_length=65)
    # office = models.ForeignKey(
    #     'Office',
    #     on_delete=models.SET_NULL,
    #     null=True, blank=True,
    #     verbose_name=_("Офис")
    # )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Организация")
        verbose_name_plural = _("Организация")


class Office(models.Model):
    firm = models.ForeignKey(
            'Organization',
            on_delete=models.SET_NULL,
            null=True, blank=True,
            verbose_name=_("Организация")
        )
    employee = models.ManyToManyField(
        User,
        # on_delete=models.SET_NULL,
        # null=True,
        # blank=True,
        verbose_name=_("Сотрудник")
    )
    # phone = models.ForeignKey(
    #     PhoneNumber,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("Телефон")
    # )
    # firm = models.CharField(
    #     max_length=240,
    #     null=True, blank=True,
    #     verbose_name=_("Организация")
    # )
    address = models.CharField(_("Адрес"), max_length=65, blank=True, null=True)
    room = models.PositiveSmallIntegerField(_("Кабинет"))

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _("Офис")
        verbose_name_plural = _("Офисы")
