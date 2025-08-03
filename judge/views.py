from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from problems.models import Problem
from submissions.models import Submission
from submissions.executor import CodeExecutor
import json
import tempfile
import subprocess
import time
import os


def safe_delete(filepath, max_retries=3, delay=0.1):
    """Safely delete a file with retries for Windows"""
    for attempt in range(max_retries):
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
            return True
        except (OSError, PermissionError) as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                continue
            else:
                print(f"Warning: Could not delete {filepath}: {e}")
                return False
    return True


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
    recent_submissions = user_submissions[:10]
    
    solved_problems = Problem.objects.filter(
        submission__user=request.user,
        submission__verdict='AC'
    ).distinct()
    
    # Calculate acceptance rate
    total_submissions = user_submissions.count()
    accepted_submissions = user_submissions.filter(verdict='AC').count()
    acceptance_rate = (accepted_submissions / total_submissions * 100) if total_submissions > 0 else 0
    
    # Get recommended problems (problems not solved yet)
    recommended_problems = Problem.objects.filter(
        is_active=True
    ).exclude(
        submission__user=request.user,
        submission__verdict='AC'
    ).order_by('difficulty', '-created_at')[:5]
    
    # Calculate current streak (simplified - consecutive days with accepted submissions)
    current_streak = 0  # This could be enhanced with actual streak calculation
    
    context = {
        'recent_submissions': recent_submissions,
        'solved_problems': solved_problems,
        'total_submissions': total_submissions,
        'solved_count': solved_problems.count(),
        'acceptance_rate': acceptance_rate,
        'current_streak': current_streak,
        'recommended_problems': recommended_problems,
    }
    return render(request, 'judge/dashboard.html', context)


def about(request):
    """About page"""
    return render(request, 'judge/about.html')


class OnlineCompilerView(View):
    """Online compiler for testing code without submitting"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        """Handle code compilation and execution"""
        try:
            data = json.loads(request.body)
            language = data.get('language')
            source_code = data.get('source_code')
            input_data = data.get('input_data', '')
            
            if not language or not source_code:
                return JsonResponse({
                    'success': False,
                    'error': 'Language and source code are required'
                })
            
            # Execute the code
            result = self._execute_code(language, source_code, input_data)
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    def _execute_code(self, language, source_code, input_data):
        """Execute code and return results"""
        try:
            if language == 'python':
                return self._execute_python(source_code, input_data)
            elif language == 'cpp':
                return self._execute_cpp(source_code, input_data)
            elif language == 'c':
                return self._execute_c(source_code, input_data)
            elif language == 'java':
                return self._execute_java(source_code, input_data)
            else:
                return {
                    'success': False,
                    'error': 'Unsupported language'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _execute_python(self, source_code, input_data):
        """Execute Python code"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(source_code)
            f.flush()
            
            try:
                start_time = time.time()
                result = subprocess.run(
                    ['python', f.name],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=5  # 5 second timeout for compiler
                )
                exec_time = int((time.time() - start_time) * 1000)
                
                if result.returncode != 0:
                    return {
                        'success': False,
                        'error': result.stderr,
                        'execution_time': exec_time
                    }
                
                return {
                    'success': True,
                    'output': result.stdout,
                    'execution_time': exec_time,
                    'memory_used': 0  # Simplified
                }
                
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'error': 'Time Limit Exceeded (5s)',
                    'execution_time': 5000
                }
            finally:
                safe_delete(f.name)
    
    def _execute_cpp(self, source_code, input_data):
        """Execute C++ code"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as source_file:
            source_file.write(source_code)
            source_file.flush()
            
            executable = source_file.name.replace('.cpp', '.exe' if os.name == 'nt' else '')
            
            try:
                # Compile
                compile_result = subprocess.run(
                    ['g++', '-o', executable, source_file.name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if compile_result.returncode != 0:
                    return {
                        'success': False,
                        'error': f'Compilation Error:\n{compile_result.stderr}',
                        'compilation_error': True
                    }
                
                # Execute
                start_time = time.time()
                result = subprocess.run(
                    [executable],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                exec_time = int((time.time() - start_time) * 1000)
                
                if result.returncode != 0:
                    return {
                        'success': False,
                        'error': result.stderr,
                        'execution_time': exec_time
                    }
                
                return {
                    'success': True,
                    'output': result.stdout,
                    'execution_time': exec_time,
                    'memory_used': 0
                }
                
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'error': 'Time Limit Exceeded (5s)',
                    'execution_time': 5000
                }
            finally:
                safe_delete(source_file.name)
                safe_delete(executable)
    
    def _execute_c(self, source_code, input_data):
        """Execute C code"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as source_file:
            source_file.write(source_code)
            source_file.flush()
            
            executable = source_file.name.replace('.c', '.exe' if os.name == 'nt' else '')
            
            try:
                # Compile
                compile_result = subprocess.run(
                    ['gcc', '-o', executable, source_file.name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if compile_result.returncode != 0:
                    return {
                        'success': False,
                        'error': f'Compilation Error:\n{compile_result.stderr}',
                        'compilation_error': True
                    }
                
                # Execute
                start_time = time.time()
                result = subprocess.run(
                    [executable],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                exec_time = int((time.time() - start_time) * 1000)
                
                if result.returncode != 0:
                    return {
                        'success': False,
                        'error': result.stderr,
                        'execution_time': exec_time
                    }
                
                return {
                    'success': True,
                    'output': result.stdout,
                    'execution_time': exec_time,
                    'memory_used': 0
                }
                
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'error': 'Time Limit Exceeded (5s)',
                    'execution_time': 5000
                }
            finally:
                safe_delete(source_file.name)
                safe_delete(executable)
    
    def _execute_java(self, source_code, input_data):
        """Execute Java code"""
        import re
        class_match = re.search(r'public\s+class\s+(\w+)', source_code)
        if not class_match:
            return {
                'success': False,
                'error': 'No public class found in Java code'
            }
        
        class_name = class_match.group(1)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file = os.path.join(temp_dir, f"{class_name}.java")
            
            with open(java_file, 'w') as f:
                f.write(source_code)
            
            try:
                # Compile
                compile_result = subprocess.run(
                    ['javac', java_file],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=temp_dir
                )
                
                if compile_result.returncode != 0:
                    return {
                        'success': False,
                        'error': f'Compilation Error:\n{compile_result.stderr}',
                        'compilation_error': True
                    }
                
                # Execute
                start_time = time.time()
                result = subprocess.run(
                    ['java', '-cp', temp_dir, class_name],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                exec_time = int((time.time() - start_time) * 1000)
                
                if result.returncode != 0:
                    return {
                        'success': False,
                        'error': result.stderr,
                        'execution_time': exec_time
                    }
                
                return {
                    'success': True,
                    'output': result.stdout,
                    'execution_time': exec_time,
                    'memory_used': 0
                }
                
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'error': 'Time Limit Exceeded (5s)',
                    'execution_time': 5000
                }


@csrf_exempt
def compile_and_run(request):
    """API endpoint for online compiler"""
    if request.method == 'POST':
        compiler = OnlineCompilerView()
        return compiler.post(request)
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST method allowed'
    })


@login_required
@csrf_exempt
def test_against_samples(request, slug):
    """Test code against sample test cases"""
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Only POST method allowed'
        })
    
    try:
        problem = get_object_or_404(Problem, slug=slug, is_active=True)
        data = json.loads(request.body)
        
        language = data.get('language')
        source_code = data.get('source_code')
        
        if not language or not source_code:
            return JsonResponse({
                'success': False,
                'error': 'Language and source code are required'
            })
        
        # Create a temporary submission for testing
        temp_submission = Submission(
            user=request.user,
            problem=problem,
            language=language,
            source_code=source_code,
            verdict='PE'
        )
        
        # Test using online compiler
        compiler = OnlineCompilerView()
        test_cases = problem.test_cases.all()[:2]  # Test first 2 test cases
        
        results = []
        all_passed = True
        
        for i, test_case in enumerate(test_cases, 1):
            result = compiler._execute_code(language, source_code, test_case.input_data)
            
            if result['success']:
                actual_output = result['output'].strip()
                expected_output = test_case.expected_output.strip()
                passed = actual_output == expected_output
            else:
                passed = False
            
            results.append({
                'test_case': i,
                'passed': passed,
                'input': test_case.input_data,
                'expected': test_case.expected_output,
                'output': result.get('output', ''),
                'execution_time': result.get('execution_time', 0),
                'error': result.get('error', '')
            })
            
            if not passed:
                all_passed = False
        
        return JsonResponse({
            'success': True,
            'all_passed': all_passed,
            'results': results
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
