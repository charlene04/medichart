from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_practitioner = models.BooleanField(default=False)


class Profile(models.Model):
    user                = models.ForeignKey(User, related_name= 'maps', on_delete = models.CASCADE)
    age                 = models.IntegerField(null=True)
    sex                 = models.CharField(max_length=60, null=True)
    marital_status      = models.CharField(max_length=60, null=True)
    religion            = models.CharField(max_length=60, null=True)
    occupation          = models.CharField(max_length=100, null=True)
    nationality         = models.CharField(max_length=30, null=True)
    state               = models.CharField(max_length=30, null=True)
    address             = models.TextField(null=True)
    next_of_kin         = models.CharField(max_length=30, null=True)
    nok_phone           = models.CharField(max_length=30, null=True)
    disease             = models.CharField(max_length=200, null=True)
    last_visit          = models.DateTimeField(null=True)
    blood_group         = models.CharField(max_length=30, null=True)
    genotype            = models.CharField(max_length=30, null=True)
    height              = models.IntegerField(null=True)
    weight              = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.email


