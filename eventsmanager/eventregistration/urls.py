from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerPage, name='userRegister'),
    path('login/', views.loginPage, name='userLogin'),
    path('logout/', views.logoutUser, name='userLogout'),
    path('profile/', views.profile, name='userProfile'),
    path('event_manager/', views.event_manager, name='userEvent_manager'),
    path('event_register/<str:pk>', views.event_register, name='event_register'),
    path('event_unregister/<str:pk>', views.event_unregister, name='event_unregister'),
]