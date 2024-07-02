from django import forms
from .models import Users, MyCars, FuelRecords, User, CarModels
from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.ModelForm):
    email = forms.EmailField(label = 'メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['email','password']
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
        
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
        widgets = {
            'target_fuel_efficiency': forms.NumberInput(attrs={'step': '0.1'}),
        }
        
class RecordsForm(forms.ModelForm):
    created_at = forms.DateTimeField(label = '', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    distance = forms.FloatField(label = '走行距離')
    fuel_amount = forms.FloatField(label = '給油量')
    
    
    class Meta:
        model = FuelRecords
        fields = [ 'distance', 'fuel_amount', ]
        
class MyCarDetailForm(forms.ModelForm):
    manufacturers = forms.ChoiceField(label = 'メーカー')
    choices=[
        ('toyota', 'トヨタ', 'TOYOTA', 'とよた', '豊田'),
        ('honda', 'ホンダ', 'HONDA', 'ほんだ', '本田'),
        ('daihatsu', 'ダイハツ', 'DAIHATSU'),
        ('nissan', 'ニッサン', 'NISSAN', '日産'),
    ]
    car_model_name = forms.ChoiceField(label= '車種')
    choices=[
        ('model_a','モデルA')
             
         ]
    engine_type = forms.ChoiceField(label='エンジン')
    choices=[
        ('gasoline', 'ガソリン'),
        ('hybrid', 'ハイブリッド'),
        ('other', 'その他'),
    ]
    color = forms.ChoiceField(label='カラー')
    choices=[
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
    purchase_on = forms.DateField(label='購入年月')
    
    class Meta:
        model = CarModels
        fields = [ 'car_model_name', 'engine_type', 'color' ]
        
class MyPageEditForm(forms.ModelForm):
    user_name = forms.CharField(label = '名前/ニックネーム')
    licence_expiry = forms.DateField(label = '運転免許証')
    next_oil_change_on = forms.DateField(label = 'オイル交換')
    next_inspection_on = forms.DateField(label = '車検')
    
    class Meta:
        model = MyCars
        fields = ['next_oil_change_on', 'next_inspection_on']
        


    

    
    