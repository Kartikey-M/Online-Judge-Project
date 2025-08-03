from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Submission, TestCaseResult
from .executor import CodeExecutor
import threading


def submission_list(request):
    """List all submissions with filters"""
    submissions = Submission.objects.all()
    
    # Filters
    user_filter = request.GET.get('user')
    problem_filter = request.GET.get('problem')
    verdict_filter = request.GET.get('verdict')
    language_filter = request.GET.get('language')
    
    if user_filter:
        submissions = submissions.filter(user__username__icontains=user_filter)
    if problem_filter:
        submissions = submissions.filter(problem__title__icontains=problem_filter)
    if verdict_filter:
        submissions = submissions.filter(verdict=verdict_filter)
    if language_filter:
        submissions = submissions.filter(language=language_filter)
    
    # Pagination
    paginator = Paginator(submissions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'verdict_choices': Submission.VERDICT_CHOICES,
        'language_choices': Submission.LANGUAGE_CHOICES,
        'filters': {
            'user': user_filter,
            'problem': problem_filter,
            'verdict': verdict_filter,
            'language': language_filter,
        }
    }
    return render(request, 'submissions/list.html', context)


def submission_detail(request, pk):
    """Submission detail view"""
    submission = get_object_or_404(Submission, pk=pk)
    
    # Check if user can view this submission
    if submission.user != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this submission.")
        return redirect('submissions:list')
    
    test_results = TestCaseResult.objects.filter(submission=submission).order_by('test_case_number')
    
    context = {
        'submission': submission,
        'test_results': test_results,
    }
    return render(request, 'submissions/detail.html', context)


@login_required
def my_submissions(request):
    """User's own submissions"""
    submissions = Submission.objects.filter(user=request.user)
    
    # Pagination
    paginator = Paginator(submissions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'submissions/my_submissions.html', context)


def judge_submission(submission_id):
    """Background task to judge a submission"""
    try:
        submission = Submission.objects.get(pk=submission_id)
        executor = CodeExecutor(submission)
        
        success, message = executor.execute()
        
        # Update submission verdict
        if success:
            submission.verdict = 'AC'
        else:
            if submission.verdict == 'PE':  # If still pending, set to WA
                submission.verdict = 'WA'
        
        submission.judged_at = timezone.now()
        submission.save()
        
    except Exception as e:
        print(f"Error judging submission {submission_id}: {e}")


def check_submission_status(request, pk):
    """AJAX endpoint to check submission status"""
    submission = get_object_or_404(Submission, pk=pk)
    
    # Check if user can view this submission
    if submission.user != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    return JsonResponse({
        'verdict': submission.verdict,
        'verdict_display': submission.verdict_display,
        'execution_time': submission.execution_time,
        'memory_used': submission.memory_used,
        'judged_at': submission.judged_at.isoformat() if submission.judged_at else None,
    })


# Signal to start judging when submission is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Submission)
def start_judging(sender, instance, created, **kwargs):
    """Start judging process when a new submission is created"""
    if created:
        # Start judging in background
        thread = threading.Thread(target=judge_submission, args=(instance.pk,))
        thread.daemon = True
        thread.start()
