from django.db import models


# Create your models here.

class Lead(models.Model):
    fio = models.CharField(verbose_name='ФИО', max_length=350)
    telephone = models.CharField(verbose_name='Телефон', max_length=50)
    address_of_lead = models.CharField(verbose_name='Адрес', max_length=350)
