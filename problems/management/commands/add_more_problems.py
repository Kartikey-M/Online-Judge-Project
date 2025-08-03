"""
Management command to add more problems with test cases
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from problems.models import Problem, TestCase
from django.utils.text import slugify

User = get_user_model()


class Command(BaseCommand):
    help = 'Add more programming problems with test cases'
    
    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        problems_data = [
            {
                'title': 'Two Sum',
                'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.''',
                'input_format': '''The first line contains an integer n, the size of the array.
The second line contains n space-separated integers representing the array.
The third line contains the target integer.''',
                'output_format': '''Output two space-separated integers representing the indices of the two numbers that add up to the target.''',
                'sample_input': '''4
2 7 11 15
9''',
                'sample_output': '''0 1''',
                'constraints': '''2 <= n <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['4', '2 7 11 15', '9'], '0 1'),
                    (['3', '3 2 4', '6'], '1 2'),
                    (['2', '3 3', '6'], '0 1'),
                    (['5', '1 2 3 4 5', '8'], '2 4'),
                    (['6', '-1 -2 -3 -4 -5 -6', '-8'], '2 4'),
                ]
            },
            {
                'title': 'Reverse String',
                'description': '''Write a function that reverses a string. The input string is given as an array of characters s.

You must do this by modifying the input array in-place with O(1) extra memory.''',
                'input_format': '''A single line containing a string of characters.''',
                'output_format': '''The reversed string.''',
                'sample_input': '''hello''',
                'sample_output': '''olleh''',
                'constraints': '''1 <= s.length <= 10^5
s[i] is a printable ASCII character.''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['hello'], 'olleh'),
                    (['Hannah'], 'hannaH'),
                    (['a'], 'a'),
                    (['ab'], 'ba'),
                    (['racecar'], 'racecar'),
                ]
            },
            {
                'title': 'Valid Parentheses',
                'description': '''Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.''',
                'input_format': '''A single line containing a string of parentheses.''',
                'output_format': '''Output "true" if the string is valid, "false" otherwise.''',
                'sample_input': '''()''',
                'sample_output': '''true''',
                'constraints': '''1 <= s.length <= 10^4
s consists of parentheses only '()[]{}'.''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['()'], 'true'),
                    (['()[]{}'], 'true'),
                    (['(]'], 'false'),
                    (['([)]'], 'false'),
                    (['{[]}'], 'true'),
                ]
            },
            {
                'title': 'Binary Search',
                'description': '''Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.''',
                'input_format': '''The first line contains an integer n, the size of the array.
The second line contains n space-separated integers in ascending order.
The third line contains the target integer.''',
                'output_format': '''Output the index of the target if found, otherwise output -1.''',
                'sample_input': '''6
-1 0 3 5 9 12
9''',
                'sample_output': '''4''',
                'constraints': '''1 <= nums.length <= 10^4
-10^4 < nums[i], target < 10^4
All the integers in nums are unique.
nums is sorted in ascending order.''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['6', '-1 0 3 5 9 12', '9'], '4'),
                    (['6', '-1 0 3 5 9 12', '2'], '-1'),
                    (['1', '5', '5'], '0'),
                    (['1', '5', '2'], '-1'),
                    (['4', '1 2 3 4', '3'], '2'),
                ]
            },
            {
                'title': 'Merge Two Sorted Lists',
                'description': '''You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

For this problem, represent the linked list as an array of integers.''',
                'input_format': '''The first line contains the size of the first list.
The second line contains the elements of the first list.
The third line contains the size of the second list.
The fourth line contains the elements of the second list.''',
                'output_format': '''Output the merged sorted list as space-separated integers.''',
                'sample_input': '''3
1 2 4
3
1 3 4''',
                'sample_output': '''1 1 2 3 4 4''',
                'constraints': '''The number of nodes in both lists is in the range [0, 50].
-100 <= Node.val <= 100
Both list1 and list2 are sorted in non-decreasing order.''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['3', '1 2 4', '3', '1 3 4'], '1 1 2 3 4 4'),
                    (['0', '', '1', '0'], '0'),
                    (['0', '', '0', ''], ''),
                    (['2', '1 3', '2', '2 4'], '1 2 3 4'),
                    (['1', '5', '1', '1'], '1 5'),
                ]
            },
            {
                'title': 'Longest Common Prefix',
                'description': '''Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".''',
                'input_format': '''The first line contains an integer n, the number of strings.
The next n lines contain the strings.''',
                'output_format': '''Output the longest common prefix.''',
                'sample_input': '''3
flower
flow
flight''',
                'sample_output': '''fl''',
                'constraints': '''1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] consists of only lowercase English letters.''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['3', 'flower', 'flow', 'flight'], 'fl'),
                    (['3', 'dog', 'racecar', 'car'], ''),
                    (['1', 'alone'], 'alone'),
                    (['2', 'prefix', 'pre'], 'pre'),
                    (['3', 'abc', 'abc', 'abc'], 'abc'),
                ]
            },
            {
                'title': 'Palindrome Number',
                'description': '''Given an integer x, return true if x is a palindrome, and false otherwise.

A palindrome number is a number that reads the same backward as forward.''',
                'input_format': '''A single integer x.''',
                'output_format': '''Output "true" if the number is a palindrome, "false" otherwise.''',
                'sample_input': '''121''',
                'sample_output': '''true''',
                'constraints': '''-2^31 <= x <= 2^31 - 1''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['121'], 'true'),
                    (['-121'], 'false'),
                    (['10'], 'false'),
                    (['0'], 'true'),
                    (['1221'], 'true'),
                ]
            },
            {
                'title': 'Remove Duplicates from Sorted Array',
                'description': '''Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.

Return the number of unique elements.''',
                'input_format': '''The first line contains an integer n, the size of the array.
The second line contains n space-separated integers in non-decreasing order.''',
                'output_format': '''Output the number of unique elements.''',
                'sample_input': '''3
1 1 2''',
                'sample_output': '''2''',
                'constraints': '''1 <= nums.length <= 3 * 10^4
-100 <= nums[i] <= 100
nums is sorted in non-decreasing order.''',
                'difficulty': 'easy',
                'time_limit': 1000,
                'memory_limit': 256,
                'test_cases': [
                    (['3', '1 1 2'], '2'),
                    (['10', '0 0 1 1 1 2 2 3 3 4'], '5'),
                    (['1', '1'], '1'),
                    (['5', '1 2 3 4 5'], '5'),
                    (['4', '1 1 1 1'], '1'),
                ]
            }
        ]
        
        self.stdout.write('Adding new problems...')
        
        for problem_data in problems_data:
            # Create the problem
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
                    'difficulty': problem_data['difficulty'],
                    'time_limit': problem_data['time_limit'],
                    'memory_limit': problem_data['memory_limit'],
                    'created_by': admin_user,
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(f'Created problem: {problem.title}')
                
                # Add test cases
                for i, (input_lines, expected_output) in enumerate(problem_data['test_cases']):
                    input_data = '\n'.join(input_lines)
                    TestCase.objects.create(
                        problem=problem,
                        input_data=input_data,
                        expected_output=expected_output,
                        is_sample=(i == 0)  # First test case is sample
                    )
                
                self.stdout.write(f'  Added {len(problem_data["test_cases"])} test cases')
            else:
                self.stdout.write(f'Problem already exists: {problem.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully added all problems!'))
