from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import (
    View
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
from .forms import MyCarDetailForm
from .forms import MyPageEditForm, MyCarsForm
from .models import Users, MyCars, FuelRecords
from .models import CarModels
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
        next_url = request.POST['next']
        if user is not None and user.is_active:
             login(request, user)
        if next_url:
             return redirect(next_url)
        return redirect('Edive:home')
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
    
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        
        try:
            user_instance = Users.objects.get(email=user.email)
            
        except Users.DoesNotExist:
            user_instance = None

        if user_instance is None:
            return render(request)
        
        try:
          my_cars = MyCars.objects.filter(user=user_instance)
        except MyCars.DoesNotExist:
            my_cars = [] 
           
        try:  
            fuel_records = FuelRecords.objects.filter(car__in=my_cars)
        except FuelRecords.DoesNotExist:
             fuel_records = []
                 
        target_achievement_count = user_instance.target_achievement_count

        for record in fuel_records:
              if record.fuel_efficiency >= record.car.target_fuel_efficiency:
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
        }

        return render(request, self.template_name, context)
        
    

    


class  MyCarView(ListView):
    template_name = 'my_car.html'
    def get(self, request, *args, **kwargs):
     return render(request,'my_car.html')
    
    
class RecordsView(CreateView, ListView, DeleteView):
    model = FuelRecords
    records = FuelRecords.objects.all()
    template_name = 'records.html'
    form_class = RecordsForm
        
    #def get(self, request,):
        # 指定された車の燃費記録を取得
       # model = FuelRecords
        #records = FuelRecords.objects.all()
        #form_class = RecordsForm()
        #return render(request, 'records.html')#, {'fuel_records': fuel_records, 'car_id': car_id})

    #def post(self, request, car_id):
        # POSTデータからフォーム入力を取得
        #distance = request.POST['distance']
        #fuel_amount = request.POST['fuel_amount']
    #    fuel_efficiency = float(distance) / float(fuel_amount)

        # 外部キーの車情報を取得
        #my_car = get_object_or_404(MyCars, id=car_id)

        # 新しい燃費記録を作成
      #  FuelRecords.objects.create(
       ##     distance=distance,
        #    fuel_amount=fuel_amount,
        #    fuel_efficiency=fuel_efficiency
        #)

        # 燃費記録の表示ページにリダイレクト
        #return redirect('records', car_id=car_id)
    
class TargetFuelView(UpdateView, DetailView):
    model = MyCars
    form_class = TargetFuelForm
    template_name = 'target_fuelefficiency.html'
    context_object_name = 'my_car'
    
        
   # def form_valid(self, form):
    #    self.object = form.save()
   #     return redirect('home')  # ホーム画面にリダイレクト


    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['car_models'] = CarModels.objects.all()
        #try:
        # my_car = self.get_object()
        # context['car_model_name'] = my_car.car_model.car_model_name
        #except MyCars.DoesNotExist:
        #   raise Http404("Car not found")
   #     return context  
   

    
class MyCarCreateView(CreateView):
    model = MyCars
    template_name = 'mycar_detail.html'
    form_class = MyCarDetailForm
    success_url = reverse_lazy('my_car.html')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
    #    return redirect('target_fuel_efficiency', pk=self.object.pk)
    
class MyCarUpdateView(UpdateView):
    model = MyCars
    #template_name = 'mycar_detail.html'
    form_class = MyCarDetailForm
    success_url = reverse_lazy('my_car.html')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
    #    return redirect('target_fuel_efficiency', pk=self.object.pk)

class MyCarDetailView(CreateView):
    model = MyCars
    template_name = 'mycar_detail.html'
    success_url = reverse_lazy('Edrive:my_car')
    fields = '__all__'
    #def get(self, request, pk):
        #my_car = get_object_or_404(MyCars, pk=pk)
        #car_model = my_car.car_model
        #form = forms.MyCarDetailForm(instance=my_car)
        #context = {
        #    'form': form
        #}

    #return render(request, 'mycar_detail.html')#, {'form': form, 'my_car': my_car, 'car_model': car_model})
    
    #def post(self, request, pk):
    #    my_car = get_object_or_404(MyCars, pk=pk)
    #    form = MyCarDetailForm(request.POST, instance=my_car)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('my_car')  # 'my_car_list' はリダイレクト先のURLのname
    #    car_model = my_car.car_model
    #    return render(request, 'mycar_detail.html', {'form': form, 'my_car':my_car, 'car_model':car_model})

mycar_detailview = MyCarDetailView.as_view()
    
class MyPageView(DetailView):
    model = Users
    template_name = 'mypage.html'
    context_object_name = 'user'
    
    def get_object(self, queryset=None):
        # ログインユーザーの情報を返します
        return self.request.user
    def get(self, request, *args, **kwargs):
        return render(request,'mypage.html')
    
class MyPageEditView(FormView):
    template_name = 'mypage_edit.html'
    def get(self, request, *args, **kwargs):
       # return render(request,'mypage_edit.html')
    
     #user_instance = Users.objects.get(pk=request.user.pk)  # ユーザーインスタンスを取得する例
     my_page_form = MyPageEditForm#(instance=user_instance)
     my_cars_form = MyCarsForm()

     context = {
            'my_page_form': my_page_form,
            'my_cars_form': my_cars_form,
        }

     return render(request, 'mypage_edit.html', context)

    def post(self, request, *args, **kwargs):
       # user_instance = Users.objects.get(pk=request.user.pk)
        #my_page_form = MyPageEditForm(request.POST, instance=user_instance)
        #my_cars_form = MyCarsForm(request.POST)

        ##    my_page_form.save()
        #    my_cars_form.save()
            # 保存後の処理やリダイレクトを行う

        context = {
        #    'my_page_form': my_page_form,
        #    'my_cars_form': my_cars_form,
        }

        return render(request, 'my_template.html', context)
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
    