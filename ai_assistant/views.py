"""
Views for AI Assistant functionality.
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging

from problems.models import Problem
from submissions.models import Submission
from .gemini_service import gemini_service

logger = logging.getLogger(__name__)


@login_required
@require_POST
def get_problem_hint(request, problem_id):
    """
    Get an AI-generated hint for a specific problem.
    """
    try:
        problem = get_object_or_404(Problem, id=problem_id)
        
        # Generate hint using Gemini
        hint = gemini_service.generate_problem_hint(
            problem_title=problem.title,
            problem_description=problem.description,
            difficulty=problem.difficulty
        )
        
        if hint:
            return JsonResponse({
                'success': True,
                'hint': hint
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Unable to generate hint at this time. Please try again later.'
            })
            
    except Problem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Problem not found.'
        })
    except Exception as e:
        logger.error(f"Error getting problem hint: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while generating the hint.'
        })


@login_required
@require_POST
def analyze_submission(request, submission_id):
    """
    Analyze a failed submission and provide debugging suggestions.
    """
    try:
        submission = get_object_or_404(Submission, id=submission_id, user=request.user)
        problem = submission.problem
        
        analysis = None
        
        if submission.verdict == 'WA':  # Wrong Answer
            analysis = gemini_service.analyze_wrong_answer(
                problem_title=problem.title,
                problem_description=problem.description,
                user_code=submission.code,
                language=submission.language,
                expected_output=None,  # We might not have this readily available
                actual_output=None     # We might not have this readily available
            )
        elif submission.verdict == 'RE':  # Runtime Error
            analysis = gemini_service.analyze_runtime_error(
                problem_title=problem.title,
                user_code=submission.code,
                language=submission.language,
                error_message=submission.error_message if hasattr(submission, 'error_message') else None
            )
        elif submission.verdict == 'TLE':  # Time Limit Exceeded
            analysis = gemini_service.analyze_time_limit_exceeded(
                problem_title=problem.title,
                user_code=submission.code,
                language=submission.language
            )
        else:
            return JsonResponse({
                'success': False,
                'error': 'Analysis is only available for Wrong Answer, Runtime Error, and Time Limit Exceeded verdicts.'
            })
        
        if analysis:
            return JsonResponse({
                'success': True,
                'analysis': analysis,
                'verdict': submission.verdict
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Unable to analyze submission at this time. Please try again later.'
            })
            
    except Submission.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Submission not found or you do not have permission to view it.'
        })
    except Exception as e:
        logger.error(f"Error analyzing submission: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while analyzing the submission.'
        })


@login_required
def ai_help_page(request):
    """
    Display the AI help page with usage information.
    """
    return render(request, 'ai_assistant/help.html')


@login_required
@require_POST
def analyze_test_failures(request):
    """
    Analyze failed test cases and provide debugging suggestions.
    """
    try:
        data = json.loads(request.body)
        problem_id = data.get('problem_id')
        language = data.get('language')
        source_code = data.get('source_code')
        failed_test_cases = data.get('failed_test_cases', [])
        
        if not all([problem_id, language, source_code, failed_test_cases]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required data for analysis.'
            })
        
        problem = get_object_or_404(Problem, id=problem_id)
        
        # Prepare test case details for analysis
        test_cases_info = ""
        for i, case in enumerate(failed_test_cases, 1):
            test_cases_info += f"""
Test Case {i}:
Input: {case.get('input', 'N/A')}
Expected Output: {case.get('expected', 'N/A')}
Your Output: {case.get('actual', 'N/A')}
"""
        
        # Generate analysis using Gemini
        analysis = gemini_service.analyze_wrong_answer(
            problem_title=problem.title,
            problem_description=problem.description,
            user_code=source_code,
            language=language,
            expected_output=test_cases_info,
            actual_output="See test cases above for detailed comparison"
        )
        
        if analysis:
            return JsonResponse({
                'success': True,
                'analysis': analysis
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Unable to analyze test failures at this time. Please try again later.'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        })
    except Problem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Problem not found.'
        })
    except Exception as e:
        logger.error(f"Error analyzing test failures: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while analyzing test failures.'
        })
