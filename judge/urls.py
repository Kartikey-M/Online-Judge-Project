from django.urls import path
from . import views

app_name = 'judge'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('compiler/', views.compile_and_run, name='compile_run'),
    path('test/<slug:slug>/', views.test_against_samples, name='test_samples'),
]
