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
from .models import User, MyCars, FuelRecords
from .models import CarModels, Manufacturers
from .models import FuelRecords
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

Users = get_user_model()

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
    #def form_valid(self, form):
    #    email = form.cleaned_data.get('email')
    #    password = form.cleaned_data.get('password')
    #    try:
    #        user = User.objects.get(email=email)
    #        if user.check_password(password):
    #            login(self.request, user)
    #            return HttpResponseRedirect(self.get_success_url())
    #        else:
    #            return self.form_invalid(form)
    #    except User.DoesNotExist:
    #        return self.form_invalid(form)

    #def get_success_url(self):
    #    return reverse_lazy('home')
    

    
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
        
        
        my_cars = MyCars.objects.filter(user=user_instance)
        fuel_records = FuelRecords.objects.filter(my_car__in=my_cars)
        
        
          
        
        target_achievement_count = user_instance.target_achievement_count

        for record in fuel_records:
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

        context = {
            'user': user_instance,
            'my_cars': my_cars,
            'fuel_records': fuel_records,
            'target_achievement_count': target_achievement_count,
        }

        return render(request, self.template_name, context)
        
    

    


class  MyCarView(LoginRequiredMixin,View):
    template_name = 'my_car.html'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_instance = Users.objects.get(email=user.email)
        my_car = MyCars.objects.filter(user=user_instance).first()
        
        context = {
             'user':user_instance,
             'mycars_instance': my_car,
        }
        return render(request, self.template_name, context)
    
    
class RecordsView(UpdateView, DetailView):
    model = FuelRecords
    #records = FuelRecords.objects.all()
    template_name = 'records.html'
    form_class = RecordsForm
        
    def get(self, request, pk):
        my_cars = get_object_or_404(MyCars, id=pk)
        fuel_records = FuelRecords.objects.filter(my_car=my_cars)
        form = RecordsForm()
        return render(request, self.template_name, {'fuel_records': fuel_records, 'form': form, 'car_id': pk})

    def post(self, request, pk):
        if 'delete_record_id' in request.POST:
            record_id = request.POST['delete_record_id']
            FuelRecords.objects.filter(id=record_id).delete()
         #POSTデータからフォーム入力を取得
        else:
         distance = float(request.POST['distance'])
         fuel_amount = float(request.POST['fuel_amount'])
         fuel_efficiency = float(distance) / float(fuel_amount)
         my_cars = get_object_or_404(MyCars, id=pk)
         FuelRecords.objects.create(
            my_car=my_cars,
            distance=distance,
            fuel_amount=fuel_amount,
            fuel_efficiency=fuel_efficiency
        )
         # 燃費記録の表示ページにリダイレクト
        return redirect('Edrive:records', pk=pk)
    
class TargetFuelView(LoginRequiredMixin, UpdateView):
    #model = MyCars
    template_name = 'target_fuelefficiency.html'
    #context_object_name = 'my_car'
     
    def get(self, request, pk):
        car_model = CarModels.objects.get(pk=pk)
        average_fuel_efficiency = car_model.average_fuel_efficiency
        # ここで平均燃費量を取得する属性を確認してください
        my_car = MyCars.objects.get(car_model=car_model, user=request.user)  # MyCarsモデルから対象の車両を取得
        form = TargetFuelForm(instance=my_car) 
        user_cars = MyCars.objects.filter(user=request.user).select_related('car_model')
        context = {
            'car_model': car_model,
            'average_fuel_efficiency': average_fuel_efficiency,
            'form':form,
            'user_cars': user_cars,  # ユーザーが登録した車種をコンテキストに追加 
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        car_model = CarModels.objects.get(pk=pk)
        my_car = MyCars.objects.get(car_model=car_model, user=request.user)
        form = TargetFuelForm(request.POST, instance=my_car)
        
        if form.is_valid():
            form.save()  # フォームの内容を保存
            return redirect('Edrive:home')  # ホーム画面にリダイレクト
        # フォームが無効な場合は再度フォームとデータをレンダリング
        car_model = CarModels.objects.get(pk=pk)
        average_fuel_efficiency = car_model.average_fuel_efficiency  # 平均燃費量を取得
        user_cars = MyCars.objects.filter(user=request.user).select_related('car_model') 
        context = {
            'car_model': car_model,
            'average_fuel_efficiency': average_fuel_efficiency,
            'form': form,
            'user_cars': user_cars,
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
        user = self.get_object()
        mycars_instance = MyCars.objects.filter(user=user).first()
        
        if mycars_instance:
            car_model = mycars_instance.car_model      
            form1 = MyCarDetailForm(instance=car_model)
            form2 = MyCarDeForm(instance=mycars_instance)
        else:
            form1 = MyCarDetailForm()
            form2 = MyCarDeForm()
            
        return render(request, self.template_name,{'form1': form1, 'form2': form2, 'mycars_instance': mycars_instance})
        
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        mycars_instance = MyCars.objects.filter(user=user).first()
        
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
        
        return render(request, self.template_name,{'form1': form1, 'form2': form2, 'mycars_instance': mycars_instance})
 
    def get_object(self):
        return User.objects.get(pk=self.kwargs['pk'])
     
    
class MyPageView(LoginRequiredMixin,View):
    template_name = 'mypage.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        user_instance = Users.objects.get(email=user.email)
        my_car = MyCars.objects.filter(user=user_instance).first()
        
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
        car_model=CarModels.objects.first()
        mycars_instance, created = MyCars.objects.get_or_create(user=user, car_model=car_model)
            
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
    