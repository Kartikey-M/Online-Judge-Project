"""
Sample data creation script for Online Judge
Run this after setting up the database to populate with sample problems
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from problems.models import Problem, TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample problems and test cases'

    def handle(self, *args, **options):
        # Create sample problems
        problems_data = [
            {
                'title': 'A+B Problem',
                'description': 'Given two integers A and B, compute A + B.',
                'input_format': 'The first line contains two integers A and B separated by a space.',
                'output_format': 'Output the sum A + B.',
                'sample_input': '3 5',
                'sample_output': '8',
                'constraints': '- -10^9 ≤ A, B ≤ 10^9',
                'time_limit': 1000,
                'memory_limit': 128,
                'difficulty': 'easy',
                'test_cases': [
                    ('3 5', '8'),
                    ('10 20', '30'),
                    ('-5 3', '-2'),
                    ('0 0', '0'),
                    ('1000000 2000000', '3000000'),
                ]
            },
            {
                'title': 'Hello World',
                'description': 'Print "Hello, World!" to the standard output.',
                'input_format': 'No input.',
                'output_format': 'Print "Hello, World!" (without quotes).',
                'sample_input': '',
                'sample_output': 'Hello, World!',
                'constraints': 'None.',
                'time_limit': 1000,
                'memory_limit': 128,
                'difficulty': 'easy',
                'test_cases': [
                    ('', 'Hello, World!'),
                ]
            },
            {
                'title': 'Maximum of Three',
                'description': 'Given three integers, find the maximum among them.',
                'input_format': 'Three integers A, B, and C separated by spaces.',
                'output_format': 'Output the maximum of the three numbers.',
                'sample_input': '3 7 5',
                'sample_output': '7',
                'constraints': '- -10^6 ≤ A, B, C ≤ 10^6',
                'time_limit': 1000,
                'memory_limit': 128,
                'difficulty': 'easy',
                'test_cases': [
                    ('3 7 5', '7'),
                    ('10 10 10', '10'),
                    ('-1 -5 -3', '-1'),
                    ('100 200 150', '200'),
                ]
            },
            {
                'title': 'Factorial',
                'description': 'Calculate the factorial of a given non-negative integer N.',
                'input_format': 'A single integer N.',
                'output_format': 'Output N! (factorial of N).',
                'sample_input': '5',
                'sample_output': '120',
                'constraints': '- 0 ≤ N ≤ 12\n- 0! = 1 by definition.',
                'time_limit': 1000,
                'memory_limit': 128,
                'difficulty': 'medium',
                'test_cases': [
                    ('5', '120'),
                    ('0', '1'),
                    ('1', '1'),
                    ('3', '6'),
                    ('10', '3628800'),
                ]
            },
            {
                'title': 'Sum of Array',
                'description': 'Given an array of N integers, calculate the sum of all elements.',
                'input_format': '- First line: integer N (size of array)\n- Second line: N integers separated by spaces',
                'output_format': 'Output the sum of all array elements.',
                'sample_input': '5\n1 2 3 4 5',
                'sample_output': '15',
                'constraints': '- 1 ≤ N ≤ 1000\n- -10^6 ≤ array elements ≤ 10^6',
                'time_limit': 2000,
                'memory_limit': 128,
                'difficulty': 'medium',
                'test_cases': [
                    ('5\n1 2 3 4 5', '15'),
                    ('3\n10 -5 7', '12'),
                    ('1\n100', '100'),
                    ('4\n0 0 0 0', '0'),
                ]
            },
            {
                'title': 'Prime Check',
                'description': 'Check if a given number is prime.',
                'input_format': 'A single integer N.',
                'output_format': 'Output "YES" if N is prime, "NO" otherwise.',
                'sample_input': '17',
                'sample_output': 'YES',
                'constraints': '- 2 ≤ N ≤ 10^6\n- A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.',
                'time_limit': 2000,
                'memory_limit': 128,
                'difficulty': 'medium',
                'test_cases': [
                    ('17', 'YES'),
                    ('4', 'NO'),
                    ('2', 'YES'),
                    ('100', 'NO'),
                    ('97', 'YES'),
                ]
            },
        ]

        self.stdout.write('Creating sample problems...')
        
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        for problem_data in problems_data:
            # Create problem
            problem, created = Problem.objects.get_or_create(
                title=problem_data['title'],
                defaults={
                    'slug': slugify(problem_data['title']),
                    'description': problem_data['description'],
                    'input_format': problem_data['input_format'],
                    'output_format': problem_data['output_format'],
                    'sample_input': problem_data['sample_input'],
                    'sample_output': problem_data['sample_output'],
                    'constraints': problem_data['constraints'],
                    'time_limit': problem_data['time_limit'],
                    'memory_limit': problem_data['memory_limit'],
                    'difficulty': problem_data['difficulty'],
                    'created_by': admin_user,
                }
            )
            
            if created:
                self.stdout.write(f'Created problem: {problem.title}')
                
                # Create test cases
                for i, (input_data, expected_output) in enumerate(problem_data['test_cases']):
                    TestCase.objects.create(
                        problem=problem,
                        input_data=input_data,
                        expected_output=expected_output,
                        is_sample=(i == 0)  # First test case is sample
                    )
                self.stdout.write(f'  Added {len(problem_data["test_cases"])} test cases')
            else:
                self.stdout.write(f'Problem already exists: {problem.title}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample problems!'))
