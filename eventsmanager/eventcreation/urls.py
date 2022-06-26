from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('event_create/', views.event_create, name='event_create'),
    path('event_manager/', views.event_manager, name='event_manager'),
    path('event_update/<str:pk>/', views.event_update, name='event_update'),
    path('event_delete/<str:pk>/', views.event_delete, name='event_delete'),
]