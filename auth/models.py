from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,


        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی", blank=True, null=True)
    introduction = models.TextField(verbose_name="معرفی", blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن", unique=True)
    active = models.BooleanField(default=False, verbose_name="فعال است؟")
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    first_login = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()   

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True  

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active 

class PhoneOTP(models.Model):
    phone       = models.CharField(max_length=11, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    validated = models.BooleanField(default = False, help_text ="We walidate this via a class in views.")

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)