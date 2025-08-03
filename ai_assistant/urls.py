"""
URL configuration for AI Assistant app.
"""
from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('hint/<int:problem_id>/', views.get_problem_hint, name='problem_hint'),
    path('analyze/<int:submission_id>/', views.analyze_submission, name='analyze_submission'),
    path('analyze-test-failures/', views.analyze_test_failures, name='analyze_test_failures'),
    path('help/', views.ai_help_page, name='help'),
]
