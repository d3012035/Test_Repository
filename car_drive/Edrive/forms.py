from django import forms
from .models import  MyCars, FuelRecords, User, CarModels, Manufacturers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    
    email = forms.EmailField(
        label = 'メールアドレス')
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput()
    )
    
        
class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前/ニックネーム')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    repassword = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password','repassword']
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class TargetFuelForm(forms.ModelForm):
    target_fuel_efficiency = forms.FloatField(label = '')

    class Meta:
        model = MyCars
        fields = ['target_fuel_efficiency']
        labels = {
            'target_fuel_efficiency':'目標燃費量(km/L)',
        }
        widgets = {
            'target_fuel_efficiency': forms.NumberInput(attrs={'step': '0.1'}),
        }
        
class RecordsForm(forms.ModelForm):
    created_at = forms.DateTimeField(label = '', widget=forms.DateInput(attrs={'type': 'date'}))
    distance = forms.FloatField(label = '走行距離')
    fuel_amount = forms.FloatField(label = '給油量')
    
    
    
    class Meta:
        model = FuelRecords
        fields = [ 'distance', 'fuel_amount']
        
class MyCarDetailForm(forms.ModelForm):
    
    
    MANUFACTURER_CHOICES = [
        ('toyota', 'トヨタ'),
        ('honda', 'ホンダ'),
        ('daihatsu', 'ダイハツ'),
        ('nissan', 'ニッサン'),
    ]  
    manufacturer_name = forms.ChoiceField(
        label = 'メーカー',
        choices=MANUFACTURER_CHOICES,          
        required=True,
        widget=forms.widgets.Select(attrs={'class': 'form-control'})
     )
    
    
    CarModel_CHOICES = [
        ('AQUA', 'アクア'),
        ('ROOMY','ルーミー'),
        ('ALPHARD','アルファード'),
        ('RAIZE', 'ライズ'),
        ('N-BOX','エヌボックス'),
        ('FREED','フリード'),
        ('VEZEL', 'ヴェゼル'),
        ('CANBUS', 'ムーヴキャンバス'),
        ('Tanto','タント'),
        ('Rocky', 'ロッキー'),
        ('NOTE', 'ノート'),
        ('SERENA','セレナ'),
        ('DAYZ','デイズ'),
        ('X-TRAIL', 'エクストレイル'),
        
    ]
    car_model_name = forms.ChoiceField(
        label= '車種',
        choices=CarModel_CHOICES,
        required=True,
        widget=forms.widgets.Select(attrs={'class':'form-control'})
        )
    
    EngineType_CHOICES = [
        ('gasoline', 'ガソリン'),
        ('hybrid', 'ハイブリッド'),
        ('other', 'その他'),
    ]
    engine_type = forms.ChoiceField(
        label='エンジン',
        choices=EngineType_CHOICES,
        required=True,
        widget=forms.widgets.Select(attrs={'class':'form-control'})
        )
    
    Color_CHOICES = [ 
        ('red', 'レッド'),
        ('blue','ブルー'),
        ('white','ホワイト'),
        ('yellow', 'イエロー'),
        ('pink', 'ピンク'),
        ('green', 'グリーン'),
        ('black', 'ブラック'),
        ('purple', 'パープル'),
        ('grey', 'グレー'),
        ('brown', 'ブラウン'),
        
    ]
    color = forms.ChoiceField(
        label='カラー',
        choices=Color_CHOICES,
        required=True,
        widget=forms.widgets.Select(attrs={'class':'form-control'})
        )
    
    class Meta:
        model = CarModels
        fields = [ 'manufacturer_name', 'car_model_name', 'engine_type', 'color' ]
        
    def __init__(self, *args, **kwargs):
        super(MyCarDetailForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['manufacturer_name'].initial = self.instance.manufacturer.manufacturer_name

    def save(self, commit=True):
        instance = super(MyCarDetailForm, self).save(commit=False)
        manufacturer_name = self.cleaned_data['manufacturer_name']
        manufacturer, created = Manufacturers.objects.get_or_create(manufacturer_name=manufacturer_name)
        instance.manufacturer = manufacturer
        if commit:
            instance.save()
        return instance
        
class MyCarDeForm(forms.ModelForm):
    purchase_on = forms.DateField(label = '購入年月', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    
    class Meta:
        model = MyCars
        fields = ['purchase_on']
            
class MyPageEditForm(forms.ModelForm):
    user_name = forms.CharField(label = '名前/ニックネーム', max_length=50, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    licence_expiry_on = forms.DateField(label = '運転免許証', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    
    
    class Meta:
        model = User
        fields = ['user_name', 'licence_expiry_on']

class MyCarsForm(forms.ModelForm):
    next_oil_change_on = forms.DateField(label='オイル交換', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    next_inspection_on = forms.DateField(label='車検', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))

    class Meta:
        model = MyCars
        fields = ['next_oil_change_on', 'next_inspection_on']
        


    

    
    