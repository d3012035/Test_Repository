from django import forms
from .models import  MyCar, FuelRecord, User, CarModel, Manufacturer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

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
        model = MyCar
        fields = ['target_fuel_efficiency']
        labels = {
            'target_fuel_efficiency':'目標燃費量(km/L)',
        }
        widgets = {
            'target_fuel_efficiency': forms.NumberInput(attrs={'step': '0.1'}),
        }
        
        
    def clean(self):
        cleaned_data = super().clean()
        # インスタンスが存在しない場合はスキップ
        if not self.instance.pk:
            return cleaned_data

        # インスタンスに関連するユーザーをチェック
        if not self.instance.user:
            raise ValidationError('関連するユーザーが存在しません。')
        
        return cleaned_data
    
    
class RecordsForm(forms.ModelForm):
    distance = forms.FloatField(label = '走行距離(km)', min_value=1.0, max_value=3000.0, error_messages={
        'min_value': '距離は1以上でなければなりません。',
        'max_value': '距離は3000以下でなければなりません。',
        })
    fuel_amount = forms.FloatField(label = '給油量(L)',min_value=1.0, max_value=200.0, error_messages={
        'min_value': '給油量は1以上でなければなりません。',
        'max_value': '給油量は200以下でなければなりません。',
        
        })
    date = forms.DateField(label = '', widget=forms.DateInput(attrs={'type': 'date'}))
    
    
    class Meta:
        model = FuelRecord
        fields = [ 'date','distance', 'fuel_amount']
        
    
        
class MyCarDetailForm(forms.ModelForm):
    
    #manufacturer_id = forms.ModelChoiceField(
    #    label = 'メーカー',
    #    queryset=Manufacturer.objects.all(),
                
    #    required=True,
    #    widget=forms.widgets.Select(attrs={'class': 'form-control'})
    #)
    
    
    
    car_model = forms.ModelChoiceField(
        label= '車種',
        queryset=CarModel.objects.all(),
        
        required=True,
        widget=forms.widgets.Select(attrs={'class':'form-control'})
    )
    
    
        
    def __init__(self, *args, **kwargs):
        super(MyCarDetailForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super(MyCarDetailForm, self).save(commit=False)
    
        if commit:
            instance.save()
        return instance
    
    purchase_on = forms.DateField(label = '購入年月', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    
    class Meta:
        model = MyCar
        fields = ['car_model', 'purchase_on']
            

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
        model = MyCar
        fields = ['next_oil_change_on', 'next_inspection_on']
        


    

    
    