from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import (
    View, TemplateView
)
from . import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistForm
from .forms import LoginForm
from .forms import TargetFuelForm
from .forms import RecordsForm
from .forms import MyCarDetailForm, MyCarDeForm
from .forms import MyPageEditForm, MyCarsForm
from .models import User, MyCar
from .models import CarModel, Manufacturer
from .models import FuelRecord
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponseNotFound
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm




Users = get_user_model()

class PortfolioView(TemplateView):
    template_name = 'portfolio.html'
    


class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('Edrive:login')
    
class UserView(View):
    
    def get(self, request, *args, **kwargs):
        
        return render(request,'start.html')

User = get_user_model()

    
class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'home.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        next_url = request.GET.get('next')
        if user is not None and user.is_active:
             login(request, user)
        if next_url:
             return redirect(next_url)
        return redirect('Edrive:home')

    
class HomeView(LoginRequiredMixin,View):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        
        try:
            user_instance = Users.objects.get(email=user.email)
            
        except Users.DoesNotExist:
            user_instance = None

        if user_instance is None:
            return render(request, self.template_name)
        
        
        my_cars = MyCar.objects.filter(user=user_instance)if MyCar.objects.filter(user=user_instance).exists() else []
        fuel_records = FuelRecord.objects.filter(my_car__user=user_instance, fuel_efficiency__isnull=False).order_by('created_at') if FuelRecord.objects.filter(my_car__user=user_instance).exists() else []
        
        target_efficiency_data = []
        achieved_efficiency_data = []
        dates = []
        
          
        
        target_achievement_count = user_instance.target_achievement_count

        for record in fuel_records:
            if record.fuel_efficiency is not None and record.my_car.target_fuel_efficiency is not None:
              if record.fuel_efficiency >= record.my_car.target_fuel_efficiency:
                target_achievement_count += 1

        if target_achievement_count >= 5:
          user_instance.driver_level += 1
          user_instance.target_achievement_count = target_achievement_count - 5  # レベルアップした分を引く
        else:
             user_instance.target_achievement_count = target_achievement_count

        user_instance.save()
        #else:
        #    my_cars = []
        #    fuel_records = []
        
        for record in fuel_records:
            target_efficiency_data.append(record.my_car.target_fuel_efficiency)
            achieved_efficiency_data.append(record.fuel_efficiency)
            dates.append(record.created_at)
            
            
            
        car_group = {
            'AQUA': 'コンパクトカー', 'ROOMY': 'コンパクトカー', 'NOTE': 'コンパクトカー',
            'ALPHARD': 'ミニバン', 'FREED': 'ミニバン', 'SERENA': 'ミニバン',
            'RAIZE': 'SUV', 'VEZEL': 'SUV', 'X-TRAIL': 'SUV', 'Rocky': 'SUV',
            'N-BOX': '軽自動車', 'CANBUS': '軽自動車', 'Tanto': '軽自動車', 'DAYZ': '軽自動車'
        }
            
        hybrid_efficiency_data = {
            'AQUA': 27.5,
            'ALPHARD': 16.68,
            'RAIZE': 25.16,
            'FREED': 18.9,
            'VEZEL': 20.65,
            'Rocky': 27.0,
            'NOTE': 23.7,
            'SERENA': 17.3,
            'DAYZ': 16.76,
            'X-TRAIL': 15.18,
        }

        gasoline_efficiency_data = {
            'AQUA': 26.8,
            'ROOMY': 26.8,
            'ALPHARD': 17.4,
            'RAIZE': 27.0,
            'N-BOX': 27.8,
            'FREED': 24.5,
            'VEZEL': 24.8,
            'CANBUS': 27.9,
            'Tanto': 27.7,
            'Rocky': 27.0,
            'NOTE': 25.9,
            'SERENA': 21.1,
            'DAYZ': 28.1,
            'X-TRAIL': 21.5,
        }
        
            
        car_models = CarModel.objects.all()
        average_fuel_efficiency = {car_model.car_model_name: car_model.average_fuel_efficiency for car_model in car_models}

        
        font_family = 'IPAexGothic'
                
        plt.switch_backend('Agg')  # バックエンドを変更
        fig, ax = plt.subplots()
        
        ax.plot( dates,target_efficiency_data, label='目標燃費')
        ax.plot(dates, achieved_efficiency_data, label='実績燃費')
        
        registered_groups = set(
            car_group.get(car.car_model.car_model_name, 'Default Value') 
            for car in my_cars 
            if car.car_model is not None
        )
        
        for model, efficiency in hybrid_efficiency_data.items():
            car_model = car_group.get(model)
            if car_model and car_model in registered_groups:
                ax.axhline(y=efficiency, color='green', linestyle='--', label=f'ハイブリッド {model} 平均燃費')


        for model, efficiency in gasoline_efficiency_data.items():
            car_model = car_group.get(model)
            if car_model and car_model in registered_groups:
                ax.axhline(y=efficiency, color='blue', linestyle='--', label=f'ガソリン {model} 平均燃費')

        
        ax.set_xlabel('日付', family=font_family, fontsize=9)
        ax.set_ylabel('燃費 (km/L)', family=font_family, fontsize=11)
        ax.set_title('燃費量',family=font_family)
        ax.legend(prop={'family': font_family})

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        #て保存し、Base64エンコードする
           
        
        context = {
            'user': user_instance,
            'my_cars': my_cars,
            'fuel_records': fuel_records,
            'target_achievement_count': target_achievement_count,
            'target_efficiency_data': target_efficiency_data,
            'achieved_efficiency_data': achieved_efficiency_data,
            'hybrid_efficiency_data': hybrid_efficiency_data,
            'gasoline_efficiency_data': gasoline_efficiency_data,
            'graph_url': graph_url,
        }

        return render(request, self.template_name, context)
        
    

    


class  MyCarView(LoginRequiredMixin,View):
    template_name = 'my_car.html'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            user_instance = Users.objects.get(email=user.email)
        except Users.DoesNotExist:
            user_instance = None

        if user_instance is None:
            return render(request, self.template_name)
        my_car = MyCar.objects.filter(user=user_instance).first()
        
        context = {
             'user':user_instance,
             'mycars_instance': my_car,
        }
        return render(request, self.template_name, context)
    
    
class RecordsView(View):
    model = FuelRecord
    template_name = 'records.html'
    form_class = RecordsForm
   
        
    def get(self, request, pk):

        user = get_object_or_404(User, pk=pk)
        # ユーザーに関連する FuelRecord を取得
        my_cars = MyCar.objects.filter(user=user)
        fuel_records = FuelRecord.objects.filter(my_car__in=my_cars)
            
        form = self.form_class()
        return render(request, self.template_name, {'fuel_records': fuel_records, 'form': form, 'car_id': pk})
        
    def post(self, request, pk):
        
        user = get_object_or_404(User, pk=pk)

        my_cars = MyCar.objects.filter(user=user)
        
        if 'delete_record_id' in request.POST:
              record_id = request.POST['delete_record_id']
              FuelRecord.objects.filter(id=record_id,my_car__in=my_cars).delete()
         #POSTデータからフォーム入力を取得
        
        form = self.form_class(request.POST)
        if form.is_valid():
                  distance = float(request.POST['distance'])
                  fuel_amount = float(request.POST['fuel_amount'])
                  fuel_efficiency = float(distance) / float(fuel_amount)
                  my_car = my_cars.first()
                  if my_car:
                    FuelRecord.objects.create(
                    my_car=my_car,    
                    distance=distance,
                    fuel_amount=fuel_amount,
                    fuel_efficiency=fuel_efficiency
                )
         # 燃費記録の表示ページにリダイレクト
        return redirect('Edrive:records', pk=pk)
    
        fuel_records = FuelRecord.objects.filter(my_car__in=my_cars)
        return render(request, self.template_name, {'fuel_records': fuel_records, 'form': form, 'car_id': pk})
        
    
class TargetFuelView(LoginRequiredMixin, UpdateView):
    #model = MyCars
    template_name = 'target_fuelefficiency.html'
    #context_object_name = 'my_car'
     
    def get(self, request, pk):
        car_model = get_object_or_404(CarModel, pk=pk)
        average_fuel_efficiency = car_model.average_fuel_efficiency
        # ここで平均燃費量を取得する属性を確認してください
        my_car = MyCar.objects.filter(car_model_id=pk, user=request.user).first()
        
        if my_car:
            form = TargetFuelForm(instance=my_car)
        else:
            form = TargetFuelForm()
        
        
        user_cars = MyCar.objects.filter(user=request.user).select_related('car_model')
        
        car_models = CarModel.objects.all()

        context = {
            'car_model': car_model,
            'average_fuel_efficiency': average_fuel_efficiency,
            'form':form,
            'user_cars': user_cars,  # ユーザーが登録した車種をコンテキストに追加 
            'car_models':car_models,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        car_model = get_object_or_404(CarModel, pk=pk)
        my_car = MyCar.objects.filter(car_model_id=pk, user=request.user).first()
        
        if my_car:
            form = TargetFuelForm(request.POST, instance=my_car)
        else:
            # 新しいレコードを作成する場合
            form = TargetFuelForm(request.POST)
            if form.is_valid():
                new_my_car = form.save(commit=False)
                new_my_car.user = request.user
                new_my_car.car_model = car_model
                new_my_car.save()
                return redirect('Edrive:home')
        
        if form.is_valid():
            form.save()  # フォームの内容を保存
            return redirect('Edrive:home')  # ホーム画面にリダイレクト
        # フォームが無効な場合は再度フォームとデータをレンダリング
        average_fuel_efficiency = car_model.average_fuel_efficiency  # 平均燃費量を取得
        user_cars = MyCar.objects.filter(user=request.user).select_related('car_model') 
        
        car_models = CarModel.objects.all()
        context = {
            'car_model': car_model,
            'average_fuel_efficiency': average_fuel_efficiency,
            'form': form,
            'user_cars': user_cars,
            'car_models': car_models,  
        }
        return render(request, self.template_name, context)

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['car_models'] = CarModels.objects.all()
        #try:
        # my_car = self.get_object()
        # context['car_model_name'] = my_car.car_model.car_model_name
        #except MyCars.DoesNotExist:
        #   raise Http404("Car not found")
   #     return context  
   

    

class MyCarDetailView(View):
    template_name = 'mycar_detail.html'
    #success_url = reverse_lazy('Edrive:my_car')
    
    def get(self, request, *args,**kwargs):
         # URL のパラメータから pk を取得
        pk = kwargs.get('pk')
        # pk でユーザーを取得
        user = get_object_or_404(User, pk=pk)
        mycars_instance = MyCar.objects.filter(user=user).first()
        
        if mycars_instance:
            car_model = mycars_instance.car_model      
            form1 = MyCarDetailForm(instance=car_model)
            form2 = MyCarDeForm(instance=mycars_instance)
        else:
            form1 = MyCarDetailForm()
            form2 = MyCarDeForm()
            
        context = {
            'form1': form1,
            'form2': form2,
            'mycars_instance': mycars_instance
        }    
            
        return render(request, self.template_name,context)
        
    
    def post(self, request, *args, **kwargs):
         # URL のパラメータから pk を取得
        pk = kwargs.get('pk')
        # pk でユーザーを取得
        user = get_object_or_404(User, pk=pk)
        mycars_instance = MyCar.objects.filter(user=user).first()
        
        if mycars_instance:
            car_model_instance = mycars_instance.car_model
            form1 = MyCarDetailForm(request.POST, instance=car_model_instance)
            form2 = MyCarDeForm(request.POST, instance=mycars_instance)
        else:
            form1 = MyCarDetailForm(request.POST)
            form2 = MyCarDeForm(request.POST)
        
        if form1.is_valid() and form2.is_valid():
            car_model = form1.save()
            mycars_instance = form2.save(commit=False)
            mycars_instance.user = user
            mycars_instance.car_model = car_model
            mycars_instance.save()
            return redirect(reverse_lazy('Edrive:my_car', kwargs={'pk':user.pk}))  
        
        context = {
            'form1': form1,
            'form2': form2,
            'mycars_instance': mycars_instance
        }
        return render(request, self.template_name,context)
 
    
class MyPageView(LoginRequiredMixin,View):
    template_name = 'mypage.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        user_instance = Users.objects.get(email=user.email)
        my_car = MyCar.objects.filter(user=user_instance).first()
        
        context = {
             'user':user_instance,
             'mycars_instance': my_car,
        }
        return render(request, self.template_name, context)
    #context_object_name = 'user'
    
    #def get_object(self, queryset=None):
        # ログインユーザーの情報を返します
    #    return self.request.user
    #def get(self, request, *args, **kwargs):
    #    return render(request,'mypage.html')
    

    
class MyPageEditView(View):
    template_name = 'mypage_edit.html'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        car_model=CarModel.objects.first()
        mycars_instance, created = MyCar.objects.get_or_create(user=user, car_model=car_model)
            
        form1 = MyPageEditForm(instance=user)
        form2 = MyCarsForm(instance=mycars_instance)
        return render(request, self.template_name, {'form1': form1, 'form2': form2, 'mycars_instance': mycars_instance})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        mycars_instance = user.mycars.first()  # リレーションされたMyCarsオブジェクトを取得

        form1 = MyPageEditForm(request.POST, instance=user)
        form2 = MyCarsForm(request.POST, instance=mycars_instance)

        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect(reverse_lazy('Edrive:mypage', kwargs={'pk': user.pk}))

        return render(request, self.template_name, {'form1': form1, 'form2': form2, 'mycars_instance': mycars_instance})

    def get_object(self):
        return User.objects.get(pk=self.kwargs['pk'])
     
       # return render(request,'mypage_edit.html')
    
     #user_instance = Users.objects.get(pk=request.user.pk)  # ユーザーインスタンスを取得する例
     #my_page_form = MyPageEditForm#(instance=user_instance)
     #my_cars_form = MyCarsForm()

     #context = {
      #      'my_page_form': my_page_form,
      #      'my_cars_form': my_cars_form,
      #  }

     #return render(request, 'mypage_edit.html', context)

    #def post(self, request, *args, **kwargs):
       # user_instance = Users.objects.get(pk=request.user.pk)
        #my_page_form = MyPageEditForm(request.POST, instance=user_instance)
        #my_cars_form = MyCarsForm(request.POST)

        ##    my_page_form.save()
        #    my_cars_form.save()
            # 保存後の処理やリダイレクトを行う

        #context = {
        #    'my_page_form': my_page_form,
        #    'my_cars_form': my_cars_form,
        #}

        #return render(request, 'mypage.html', context)
     #   user = request.user
      #  my_car = get_object_or_404(MyCars, user=user)
      #  user_form = MyPageEditForm(instance=user)
      #  car_form = MyCarsForm(instance=my_car)
      #  return render(request, self.template_name, {
      #      'user_form': user_form,
      #      'car_form': car_form,
      #  })

    #def post(self, request, *args, **kwargs):
     # user_form = MyPageEditForm(request.POST, instance=user)
     #   car_form = MyCarsForm(request.POST, instance=my_car)
        
     #   if user_form.is_valid() and car_form.is_valid():
     #       user_form.save()
     #       car_form.save()
     #       return redirect('Edrive:mypage')  # 更新後にマイページにリダイレクト
    #  return render(request, self.template_name, {
     #       'user_form': user_form,
      #      'car_form': car_form,
       # })

    
class EcoCarSiteView(View):
    template_name = 'eco_car_site.html'
    def get(self, request, *args, **kwargs):
        return render(request,'eco_car_site.html')
    