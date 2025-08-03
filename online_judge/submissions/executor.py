import os
import subprocess
import tempfile
import time
from django.conf import settings
from .models import Submission, TestCaseResult


class CodeExecutor:
    """Handle code compilation and execution"""
    
    def __init__(self, submission):
        self.submission = submission
        self.language = submission.language
        self.source_code = submission.source_code
        self.problem = submission.problem
    
    def execute(self):
        """Main execution method"""
        try:
            if self.language == 'python':
                return self._execute_python()
            elif self.language == 'cpp':
                return self._execute_cpp()
            elif self.language == 'c':
                return self._execute_c()
            elif self.language == 'java':
                return self._execute_java()
            else:
                return False, "Unsupported language"
        except Exception as e:
            return False, str(e)
    
    def _execute_python(self):
        """Execute Python code"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.source_code)
            f.flush()
            
            try:
                # Run against test cases
                all_passed = True
                for i, test_case in enumerate(self.problem.test_cases.all(), 1):
                    passed, exec_time, memory, error = self._run_test_case(
                        ['python', f.name], 
                        test_case.input_data, 
                        test_case.expected_output
                    )
                    
                    # Save test result
                    TestCaseResult.objects.create(
                        submission=self.submission,
                        test_case_number=i,
                        passed=passed,
                        execution_time=exec_time,
                        memory_used=memory,
                        error_message=error
                    )
                    
                    if not passed:
                        all_passed = False
                
                return all_passed, "Execution completed"
            
            finally:
                os.unlink(f.name)
    
    def _execute_cpp(self):
        """Execute C++ code"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as source_file:
            source_file.write(self.source_code)
            source_file.flush()
            
            # Compile
            executable = source_file.name.replace('.cpp', '.exe' if os.name == 'nt' else '')
            compile_cmd = ['g++', '-o', executable, source_file.name]
            
            try:
                result = subprocess.run(
                    compile_cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                
                if result.returncode != 0:
                    self.submission.verdict = 'CE'
                    self.submission.compilation_error = result.stderr
                    self.submission.save()
                    return False, "Compilation Error"
                
                # Run against test cases
                all_passed = True
                for i, test_case in enumerate(self.problem.test_cases.all(), 1):
                    passed, exec_time, memory, error = self._run_test_case(
                        [executable], 
                        test_case.input_data, 
                        test_case.expected_output
                    )
                    
                    TestCaseResult.objects.create(
                        submission=self.submission,
                        test_case_number=i,
                        passed=passed,
                        execution_time=exec_time,
                        memory_used=memory,
                        error_message=error
                    )
                    
                    if not passed:
                        all_passed = False
                
                return all_passed, "Execution completed"
            
            finally:
                if os.path.exists(source_file.name):
                    os.unlink(source_file.name)
                if os.path.exists(executable):
                    os.unlink(executable)
    
    def _execute_c(self):
        """Execute C code - similar to C++"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as source_file:
            source_file.write(self.source_code)
            source_file.flush()
            
            executable = source_file.name.replace('.c', '.exe' if os.name == 'nt' else '')
            compile_cmd = ['gcc', '-o', executable, source_file.name]
            
            try:
                result = subprocess.run(
                    compile_cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                
                if result.returncode != 0:
                    self.submission.verdict = 'CE'
                    self.submission.compilation_error = result.stderr
                    self.submission.save()
                    return False, "Compilation Error"
                
                all_passed = True
                for i, test_case in enumerate(self.problem.test_cases.all(), 1):
                    passed, exec_time, memory, error = self._run_test_case(
                        [executable], 
                        test_case.input_data, 
                        test_case.expected_output
                    )
                    
                    TestCaseResult.objects.create(
                        submission=self.submission,
                        test_case_number=i,
                        passed=passed,
                        execution_time=exec_time,
                        memory_used=memory,
                        error_message=error
                    )
                    
                    if not passed:
                        all_passed = False
                
                return all_passed, "Execution completed"
            
            finally:
                if os.path.exists(source_file.name):
                    os.unlink(source_file.name)
                if os.path.exists(executable):
                    os.unlink(executable)
    
    def _execute_java(self):
        """Execute Java code"""
        # Extract class name from code
        import re
        class_match = re.search(r'public\s+class\s+(\w+)', self.source_code)
        if not class_match:
            return False, "No public class found"
        
        class_name = class_match.group(1)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file = os.path.join(temp_dir, f"{class_name}.java")
            
            with open(java_file, 'w') as f:
                f.write(self.source_code)
            
            # Compile
            compile_cmd = ['javac', java_file]
            result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True, 
                timeout=10,
                cwd=temp_dir
            )
            
            if result.returncode != 0:
                self.submission.verdict = 'CE'
                self.submission.compilation_error = result.stderr
                self.submission.save()
                return False, "Compilation Error"
            
            # Run against test cases
            all_passed = True
            for i, test_case in enumerate(self.problem.test_cases.all(), 1):
                passed, exec_time, memory, error = self._run_test_case(
                    ['java', '-cp', temp_dir, class_name], 
                    test_case.input_data, 
                    test_case.expected_output
                )
                
                TestCaseResult.objects.create(
                    submission=self.submission,
                    test_case_number=i,
                    passed=passed,
                    execution_time=exec_time,
                    memory_used=memory,
                    error_message=error
                )
                
                if not passed:
                    all_passed = False
            
            return all_passed, "Execution completed"
    
    def _run_test_case(self, command, input_data, expected_output):
        """Run a single test case"""
        try:
            start_time = time.time()
            
            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.problem.time_limit / 1000.0  # Convert ms to seconds
            )
            
            exec_time = int((time.time() - start_time) * 1000)  # Convert to ms
            
            if result.returncode != 0:
                return False, exec_time, 0, result.stderr
            
            # Compare output (strip whitespace)
            actual_output = result.stdout.strip()
            expected_output = expected_output.strip()
            
            if actual_output == expected_output:
                return True, exec_time, 0, ""
            else:
                return False, exec_time, 0, f"Expected: {expected_output}, Got: {actual_output}"
                
        except subprocess.TimeoutExpired:
            return False, self.problem.time_limit, 0, "Time Limit Exceeded"
        except Exception as e:
            return False, 0, 0, str(e)
