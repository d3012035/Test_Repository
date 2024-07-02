from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
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

    def get_absolute_url(self):
        return reverse_lazy('accounts:home')




class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Users(BaseModel):
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    licence_expiry_on = models.DateField()
    driver_level = models.IntegerField(default=1)
    target_achievement_count = models.IntegerField(default=0)
      
    
            
            
    class Meta:
        db_table = 'users'
        
class Manufacturers(BaseModel):
    manufacturer_name = models.CharField(max_length=70)
    
    class Meta:
        db_table = 'manufacturers'
        
    
class CarModels(BaseModel):
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.CASCADE, null=True)
    car_model_name = models.CharField(max_length=120)
    engine_type = models.CharField(max_length=50)
    color = models.CharField(max_length=150)
    avarage_fuel_efficiency = models.FloatField()
    car_group = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'car_models'
    
    
class MyCars(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModels, on_delete=models.CASCADE)
    purchase_on = models.DateField()
    next_oil_change_on = models.DateField()
    next_inspection_on = models.DateField()
    target_fuel_efficiency = models.FloatField(null=True, blank=True)
    
    
    class Meta:
        db_table = 'my_cars'
    
        
class FuelRecords(BaseModel):
    my_car = models.ForeignKey(MyCars, on_delete=models.CASCADE)
    distance = models.FloatField()
    fuel_amount = models.FloatField()
    fuel_efficiency = models.FloatField(editable=False)
    
    def save(self, *args, **kwargs):
        self.fuel_efficiency = self.distance / self.fuel_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.create_at} - {self.distance}km / {self.fuel_amount}L"
    
    class Meta:
        db_table = 'fuel_records'
        
class EcoDriveSites(BaseModel):
    ecodrive_url = models.CharField(max_length=260)
    site_title = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'eco_drive_sites'
#class Pictures(BaseModel):
    
 #   picture = models.FileField(upload_to= 'picture/')
    
    