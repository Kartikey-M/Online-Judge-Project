"""
Django management command to populate the database with sample problems.
This is essential for production deployment on Render.com where the database starts empty.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from problems.models import Problem, TestCase
from django.utils.text import slugify

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample coding problems for Code Matrix'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing problems before adding new ones',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Deleting existing problems...'))
            Problem.objects.all().delete()

        # Get or create admin user for problem creation
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@codematrix.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')  # Should be changed in production
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))

        # Sample problems data
        problems_data = [
            {
                'title': 'Two Sum',
                'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.''',
                'input_format': '''Line 1: Space-separated integers representing the array
Line 2: Target integer''',
                'output_format': 'Two space-separated integers representing the indices',
                'sample_input': '2 7 11 15\n9',
                'sample_output': '0 1',
                'constraints': '2 ≤ nums.length ≤ 10^4\n-10^9 ≤ nums[i] ≤ 10^9\n-10^9 ≤ target ≤ 10^9',
                'difficulty': 'easy',
                'test_cases': [
                    ('2 7 11 15\n9', '0 1'),
                    ('3 2 4\n6', '1 2'),
                    ('3 3\n6', '0 1'),
                ]
            },
            {
                'title': 'Palindrome Number',
                'description': '''Given an integer x, return true if x is palindrome integer.

An integer is a palindrome when it reads the same backward as forward.''',
                'input_format': 'A single integer x',
                'output_format': 'true if palindrome, false otherwise',
                'sample_input': '121',
                'sample_output': 'true',
                'constraints': '-2^31 ≤ x ≤ 2^31 - 1',
                'difficulty': 'easy',
                'test_cases': [
                    ('121', 'true'),
                    ('-121', 'false'),
                    ('10', 'false'),
                    ('0', 'true'),
                ]
            },
            {
                'title': 'Valid Parentheses',
                'description': '''Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.''',
                'input_format': 'A string containing only parentheses characters',
                'output_format': 'true if valid, false otherwise',
                'sample_input': '()',
                'sample_output': 'true',
                'constraints': '1 ≤ s.length ≤ 10^4',
                'difficulty': 'easy',
                'test_cases': [
                    ('()', 'true'),
                    ('()[]{}', 'true'),
                    ('(]', 'false'),
                    ('([)]', 'false'),
                    ('{[]}', 'true'),
                ]
            },
            {
                'title': 'Maximum Subarray',
                'description': '''Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.''',
                'input_format': '''Line 1: Integer n (length of array)
Line 2: n space-separated integers''',
                'output_format': 'Maximum sum of contiguous subarray',
                'sample_input': '9\n-2 1 -3 4 -1 2 1 -5 4',
                'sample_output': '6',
                'constraints': '1 ≤ nums.length ≤ 10^5\n-10^4 ≤ nums[i] ≤ 10^4',
                'difficulty': 'easy',
                'test_cases': [
                    ('9\n-2 1 -3 4 -1 2 1 -5 4', '6'),
                    ('1\n1', '1'),
                    ('5\n5 4 -1 7 8', '23'),
                ]
            },
            {
                'title': 'Longest Common Subsequence',
                'description': '''Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.''',
                'input_format': '''Line 1: String text1
Line 2: String text2''',
                'output_format': 'Length of longest common subsequence',
                'sample_input': 'abcde\nace',
                'sample_output': '3',
                'constraints': '1 ≤ text1.length, text2.length ≤ 1000',
                'difficulty': 'medium',
                'test_cases': [
                    ('abcde\nace', '3'),
                    ('abc\nabc', '3'),
                    ('abc\ndef', '0'),
                ]
            },
            {
                'title': 'Binary Tree Inorder Traversal',
                'description': '''Given the root of a binary tree, return the inorder traversal of its nodes' values.

For this problem, assume the tree is given as a level-order array where null values are represented as -1.''',
                'input_format': 'Space-separated integers representing level-order traversal (-1 for null)',
                'output_format': 'Space-separated integers representing inorder traversal',
                'sample_input': '1 -1 2 3',
                'sample_output': '1 3 2',
                'constraints': 'The number of nodes in the tree is in the range [0, 100]',
                'difficulty': 'medium',
                'test_cases': [
                    ('1 -1 2 3', '1 3 2'),
                    ('-1', ''),
                    ('1', '1'),
                ]
            },
            {
                'title': 'Climbing Stairs',
                'description': '''You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?''',
                'input_format': 'A single integer n',
                'output_format': 'Number of distinct ways to climb n steps',
                'sample_input': '2',
                'sample_output': '2',
                'constraints': '1 ≤ n ≤ 45',
                'difficulty': 'easy',
                'test_cases': [
                    ('2', '2'),
                    ('3', '3'),
                    ('4', '5'),
                    ('5', '8'),
                ]
            },
            {
                'title': 'Merge Two Sorted Lists',
                'description': '''You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists in a sorted list. The list should be made by splicing together the nodes of the first two lists.

For simplicity, represent linked lists as arrays.''',
                'input_format': '''Line 1: Space-separated integers for list1 (empty if no elements)
Line 2: Space-separated integers for list2 (empty if no elements)''',
                'output_format': 'Space-separated integers representing merged sorted list',
                'sample_input': '1 2 4\n1 3 4',
                'sample_output': '1 1 2 3 4 4',
                'constraints': 'The number of nodes in both lists is in the range [0, 50]',
                'difficulty': 'easy',
                'test_cases': [
                    ('1 2 4\n1 3 4', '1 1 2 3 4 4'),
                    ('\n', ''),
                    ('\n0', '0'),
                ]
            },
            {
                'title': 'Search in Rotated Sorted Array',
                'description': '''There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k. Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.''',
                'input_format': '''Line 1: Space-separated integers representing the rotated array
Line 2: Target integer''',
                'output_format': 'Index of target in array, or -1 if not found',
                'sample_input': '4 5 6 7 0 1 2\n0',
                'sample_output': '4',
                'constraints': '1 ≤ nums.length ≤ 5000\n-10^4 ≤ nums[i] ≤ 10^4',
                'difficulty': 'medium',
                'test_cases': [
                    ('4 5 6 7 0 1 2\n0', '4'),
                    ('4 5 6 7 0 1 2\n3', '-1'),
                    ('1\n0', '-1'),
                ]
            },
            {
                'title': 'Longest Palindromic Substring',
                'description': '''Given a string s, return the longest palindromic substring in s.

A string is palindromic if it reads the same forward and backward.''',
                'input_format': 'A single string s',
                'output_format': 'The longest palindromic substring',
                'sample_input': 'babad',
                'sample_output': 'bab',
                'constraints': '1 ≤ s.length ≤ 1000',
                'difficulty': 'medium',
                'test_cases': [
                    ('babad', 'bab'),
                    ('cbbd', 'bb'),
                    ('a', 'a'),
                    ('ac', 'a'),
                ]
            }
        ]

        created_count = 0
        
        for problem_data in problems_data:
            # Check if problem already exists
            if Problem.objects.filter(title=problem_data['title']).exists():
                self.stdout.write(f'Problem "{problem_data["title"]}" already exists, skipping...')
                continue

            # Create the problem
            problem = Problem.objects.create(
                title=problem_data['title'],
                slug=slugify(problem_data['title']),
                description=problem_data['description'],
                input_format=problem_data['input_format'],
                output_format=problem_data['output_format'],
                sample_input=problem_data['sample_input'],
                sample_output=problem_data['sample_output'],
                constraints=problem_data['constraints'],
                difficulty=problem_data['difficulty'],
                time_limit=5000,  # 5 seconds
                memory_limit=256,  # 256 MB
                created_by=admin_user,
                is_active=True
            )

            # Create test cases
            for i, (input_data, expected_output) in enumerate(problem_data['test_cases']):
                TestCase.objects.create(
                    problem=problem,
                    input_data=input_data,
                    expected_output=expected_output,
                    is_sample=(i == 0)  # First test case is sample
                )

            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created problem: {problem.title} ({problem.difficulty})')
            )

        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} problems with test cases!'
            )
        )
        
        total_problems = Problem.objects.count()
        self.stdout.write(f'Total problems in database: {total_problems}')
        
        if total_problems > 0:
            self.stdout.write('\nProblems by difficulty:')
            for difficulty in ['easy', 'medium', 'hard']:
                count = Problem.objects.filter(difficulty=difficulty).count()
                self.stdout.write(f'  {difficulty.title()}: {count}')
        
        self.stdout.write('\n🚀 Code Matrix is ready with sample problems!')
        self.stdout.write('Visit the admin panel or /problems/ to see them.')
