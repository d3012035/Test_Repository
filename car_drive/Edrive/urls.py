from django.urls import path
from .views import (
    UserView, LoginView, RegistUserView, HomeView,RecordsView,
    TargetFuelView, MyCarView, MyCarCreateView, MyPageView, MyPageEditView, EcoCarSiteView, MyCarUpdateView,
)
app_name = 'Edrive'

urlpatterns = [
    path('start/',UserView.as_view(), name='start'),
    path('login/',LoginView.as_view(), name='login'),
    path('regist/',RegistUserView.as_view(), name='regist'),
    path('home/',HomeView.as_view(), name = 'home'),
    path('my_car/',MyCarView.as_view(), name = 'my_car'),
    path('records/',RecordsView.as_view(), name = 'records'),
    path('target_fuelefficiency/<int:pk>',TargetFuelView.as_view(), name = 'target_fuelefficiency'),
    path('mycar/<int:pk>/edit/',MyCarUpdateView.as_view(), name = 'mycar_edit'),
    path('mycar/add/',MyCarCreateView.as_view(), name = 'mycar_add'),
    path('mypage/',MyPageView.as_view(), name = 'mypage'),
    path('mypage_edit/',MyPageEditView.as_view(), name = 'mypage_edit'),
    path('eco_car_site/',EcoCarSiteView.as_view(), name = 'eco_car_site'),
]