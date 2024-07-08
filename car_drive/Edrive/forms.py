from django import forms
from .models import  MyCars, FuelRecords, User, CarModels
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
    created_at = forms.DateTimeField(label = '', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
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
    manufacturers = forms.ChoiceField(
        label = 'メーカー',
        choices=MANUFACTURER_CHOICES,          
        required=True,
        widget=forms.widgets.Select
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
        widget=forms.widgets.Select
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
        widget=forms.widgets.Select
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
        widget=forms.widgets.Select
        )
   
    purchase_on = forms.DateField(label='購入年月')
    
    class Meta:
        model = CarModels
        fields = [ 'car_model_name', 'engine_type', 'color' ]
        
class MyPageEditForm(forms.ModelForm):
    user_name = forms.CharField(label = '名前/ニックネーム', max_length=50, required=False)
    licence_expiry_on = forms.DateField(label = '運転免許証', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ['user_name', 'licence_expiry_on']

class MyCarsForm(forms.ModelForm):
    next_oil_change_on = forms.DateField(label='オイル交換', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    next_inspection_on = forms.DateField(label='車検', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = MyCars
        fields = ['next_oil_change_on', 'next_inspection_on']
        


    

    
    