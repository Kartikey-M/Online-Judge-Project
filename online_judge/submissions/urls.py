from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('', views.submission_list, name='list'),
    path('<int:pk>/', views.submission_detail, name='detail'),
    path('my/', views.my_submissions, name='my_submissions'),
    path('<int:pk>/status/', views.check_submission_status, name='status'),
]
