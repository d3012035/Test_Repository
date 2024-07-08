from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self,  email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
       
        return user
    
def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    return self.create_user(email, password, **extra_fields)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
   
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(max_length=1000, default='default_name')
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    licence_expiry_on = models.DateField()
    driver_level = models.IntegerField(default=1)
    target_achievement_count = models.IntegerField(default=0)  
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='edrive_user_set',  # 追加
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='edrive_user_set',  # 追加
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    objects = UserManager()

    def __str__(self):
        return self.email


        
class Manufacturers(BaseModel):
    name = models.CharField(max_length=1000, default='default_name')
    manufacturer_name = models.CharField(max_length=70)
    
    class Meta:
        db_table = 'manufacturers'
        
    
class CarModels(BaseModel):
    name = models.CharField(max_length=1000, default='default_name')
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.CASCADE, null=True)
    car_model_name = models.CharField(max_length=120)
    engine_type = models.CharField(max_length=50)
    color = models.CharField(max_length=150)
    avarage_fuel_efficiency = models.FloatField()
    car_group = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'car_models'
    
    
class MyCars(BaseModel):
    name = models.CharField(max_length=1000, default='default_name')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    car_model = models.ForeignKey(CarModels, on_delete=models.CASCADE, default=1)
    purchase_on = models.DateField()
    next_oil_change_on = models.DateField()
    next_inspection_on = models.DateField()
    target_fuel_efficiency = models.FloatField(null=True, blank=True)
    
    
    class Meta:
        db_table = 'my_cars'
    
        
class FuelRecords(BaseModel):
    my_car = models.ForeignKey(MyCars, on_delete=models.CASCADE, default=1)
    distance = models.FloatField(verbose_name="走行距離 (km)")
    fuel_amount = models.FloatField(verbose_name="給油量 (L)")
    fuel_efficiency = models.FloatField(verbose_name="燃費 (km/L)", blank=True, null=True, editable=False)
    
    def save(self, *args, **kwargs):
        if self.distance and self.fuel_amount:
         self.fuel_efficiency = self.distance / self.fuel_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created_at} - {self.distance}km / {self.fuel_amount}L"
    
    class Meta:
        db_table = 'fuel_records'
        
class EcoDriveSites(BaseModel):
    ecodrive_url = models.CharField(max_length=260)
    site_title = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'eco_drive_sites'
#class Pictures(BaseModel):rate
    
 #   picture = models.FileField(upload_to= 'picture/')
    
    