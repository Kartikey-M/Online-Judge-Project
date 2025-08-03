from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('', views.my_submissions, name='list'),  # User's own submissions
    path('all/', views.submission_list, name='all'),  # All submissions (for admins)
    path('<int:pk>/', views.submission_detail, name='detail'),
    path('<int:pk>/status/', views.check_submission_status, name='status'),
]
