from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import (
    View
)
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistForm
from .forms import LoginForm
from .forms import TargetFuelForm
from .forms import RecordsForm
from .forms import MyCarDetailForm
from .forms import MyPageEditForm
from .models import Users, MyCars, User
from .models import CarModels
from .models import FuelRecords
from django.urls import reverse_lazy
from django.http import Http404

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('Edrive:login')
    
class UserView(View):
    
    def get(self, request, *args, **kwargs):
        
        return render(request,'start.html')
    
class LoginView(FormView):
    template_name = 'login.html'
    authentication_form = LoginForm
    success_url = reverse_lazy('Edrive:home')
    
    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)

    
class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        #return render(request,'home.html')
        user = request.user

        my_cars = MyCars.objects.filter(user=user)
        fuel_records = FuelRecords.objects.filter(car__in=my_cars)
        target_achievement_count = user.target_achievement_count

        for record in fuel_records:
            if record.fuel_efficiency >= record.car.target_fuel_efficiency:
                target_achievement_count += 1

        if target_achievement_count >= 5:
            user.driver_level += 1
            user.target_achievement_count = target_achievement_count - 5  # レベルアップした分を引く
        else:
            user.target_achievement_count = target_achievement_count

        user.save()

        context = {
            'user': user,
            'my_cars': my_cars,
            'fuel_records': fuel_records,
        }

        return render(request, self.template_name, context)
    
class MyCarView(ListView):
    template_name = 'my_car.html'
    def get(self, request, *args, **kwargs):
        return render(request,'my_car.html')
    
    
class RecordsView(CreateView, ListView, DeleteView):
    model = FuelRecords
    template_name = 'records.html'
    context_object_name = 'fuel_records'
    form_class = RecordsForm
    success_url = 'records.html'
   
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return self.get(request, *args, **kwargs)
   

class TargetFuelView(UpdateView, DetailView):
    model = MyCars
    form_class = TargetFuelForm
    template_name = 'target_fuelefficiency.html'
    context_object_name = 'my_car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
         my_car = self.get_object()
         context['car_model_name'] = my_car.car_model.car_model_name
         context['average_fuel_efficiency'] = my_car.car_model.average_fuel_efficiency
        except MyCars.DoesNotExist:
           raise Http404("Car not found")
        return context  
   

    
class MyCarCreateView(CreateView):
    model = MyCars
    template_name = 'mycar_detail.html'
    form_class = MyCarDetailForm
    success_url = reverse_lazy('my_car.html')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return redirect('target_fuel_efficiency', pk=self.object.pk)
    
class MyCarUpdateView(UpdateView):
    model = MyCars
    template_name = 'mycar_detail.html'
    form_class = MyCarDetailForm
    success_url = reverse_lazy('my_car.html')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return redirect('target_fuel_efficiency', pk=self.object.pk)
    
class MyPageView(View):
    template_name = 'mypage.html'
    def get(self, request, *args, **kwargs):
        return render(request,'mypage.html')
    
class MyPageEditView(FormView):
    template_name = 'mypage_edit.html'
    form_class = MyPageEditForm
    success_url = 'my_page.html'
    
class EcoCarSiteView(View):
    template_name = 'eco_car_site.html'
    def get(self, request, *args, **kwargs):
        return render(request,'eco_car_site.html')
    