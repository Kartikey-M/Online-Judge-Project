from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Problem, TestCase
from submissions.models import Submission
from submissions.forms import SubmissionForm


def problem_list(request):
    """List all active problems"""
    search_query = request.GET.get('search', '')
    difficulty = request.GET.get('difficulty', '')
    
    problems = Problem.objects.filter(is_active=True)
    
    if search_query:
        problems = problems.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if difficulty:
        problems = problems.filter(difficulty=difficulty)
    
    # Pagination
    paginator = Paginator(problems, 10)  # 10 problems per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'difficulty': difficulty,
        'difficulty_choices': Problem.DIFFICULTY_CHOICES,
    }
    return render(request, 'problems/list.html', context)


def problem_detail(request, slug):
    """Problem detail view with submission form"""
    problem = get_object_or_404(Problem, slug=slug, is_active=True)
    
    # Get sample test cases (visible to users)
    sample_cases = problem.test_cases.filter(is_sample=True).order_by('id')
    
    # Get user's previous submissions for this problem
    user_submissions = []
    if request.user.is_authenticated:
        user_submissions = Submission.objects.filter(
            user=request.user, 
            problem=problem
        ).order_by('-submitted_at')[:5]
    
    context = {
        'problem': problem,
        'sample_cases': sample_cases,
        'user_submissions': user_submissions,
        'submission_form': SubmissionForm(),
    }
    return render(request, 'problems/detail.html', context)


@login_required
def submit_solution(request, slug):
    """Handle code submission"""
    problem = get_object_or_404(Problem, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = problem
            submission.verdict = 'PE'  # Set initial status to Pending
            submission.save()  # This will trigger the post_save signal
            messages.success(request, 'Your solution has been submitted and is being judged.')
            return redirect('submissions:detail', pk=submission.pk)
        else:
            # Form is invalid, re-render the page with the form containing errors
            messages.error(request, 'Please correct the errors below.')
            
            # Get sample test cases for re-rendering
            sample_cases = problem.test_cases.filter(is_sample=True).order_by('id')
            
            user_submissions = []
            if request.user.is_authenticated:
                user_submissions = Submission.objects.filter(
                    user=request.user,
                    problem=problem
                ).order_by('-submitted_at')[:5]
            
            context = {
                'problem': problem,
                'sample_cases': sample_cases,
                'user_submissions': user_submissions,
                'submission_form': form,  # Pass the invalid form back to the template
            }
            return render(request, 'problems/detail.html', context)

    # If GET request, redirect to the problem detail page
    return redirect('problems:detail', slug=slug)
