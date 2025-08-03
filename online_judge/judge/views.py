from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from problems.models import Problem
from submissions.models import Submission


def home(request):
    """Home page view"""
    recent_problems = Problem.objects.filter(is_active=True).order_by('-created_at')[:5]
    context = {
        'recent_problems': recent_problems,
    }
    
    if request.user.is_authenticated:
        # Get user's recent submissions
        recent_submissions = Submission.objects.filter(
            user=request.user
        ).order_by('-submitted_at')[:5]
        context['recent_submissions'] = recent_submissions
    
    return render(request, 'judge/home.html', context)


@login_required
def dashboard(request):
    """User dashboard"""
    user_submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    solved_problems = Problem.objects.filter(
        submission__user=request.user,
        submission__verdict='AC'
    ).distinct()
    
    context = {
        'submissions': user_submissions[:10],  # Last 10 submissions
        'solved_problems': solved_problems,
        'total_submissions': user_submissions.count(),
        'solved_count': solved_problems.count(),
    }
    return render(request, 'judge/dashboard.html', context)


def about(request):
    """About page"""
    return render(request, 'judge/about.html')
