from django.urls import path
from . import views

app_name = 'problems'

urlpatterns = [
    path('', views.problem_list, name='list'),
    path('<slug:slug>/', views.problem_detail, name='detail'),
    path('<slug:slug>/submit/', views.submit_solution, name='submit'),
]
