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

You can return the answer in any order.

**Example 1:**
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

**Example 2:**
Input: nums = [3,2,4], target = 6
Output: [1,2]

**Example 3:**
Input: nums = [3,3], target = 6
Output: [0,1]''',
                'input_format': '''First line: Space-separated integers representing the array nums
Second line: Integer target''',
                'output_format': 'Two space-separated integers representing the indices (0-indexed)',
                'sample_input': '2 7 11 15\n9',
                'sample_output': '0 1',
                'constraints': '''• 2 ≤ nums.length ≤ 10⁴
• -10⁹ ≤ nums[i] ≤ 10⁹
• -10⁹ ≤ target ≤ 10⁹
• Only one valid answer exists''',
                'difficulty': 'easy',
                'test_cases': [
                    ('2 7 11 15\n9', '0 1'),
                    ('3 2 4\n6', '1 2'),
                    ('3 3\n6', '0 1'),
                    ('2 5 5 11\n10', '1 2'),
                ]
            },
            {
                'title': 'Palindrome Number',
                'description': '''Given an integer x, return true if x is a palindrome, and false otherwise.

An integer is a palindrome when it reads the same backward as forward.

**Example 1:**
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

**Example 2:**
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

**Example 3:**
Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.

**Follow up:** Could you solve it without converting the integer to a string?''',
                'input_format': 'A single integer x',
                'output_format': 'Output "true" if x is a palindrome, "false" otherwise',
                'sample_input': '121',
                'sample_output': 'true',
                'constraints': '''• -2³¹ ≤ x ≤ 2³¹ - 1''',
                'difficulty': 'easy',
                'test_cases': [
                    ('121', 'true'),
                    ('-121', 'false'),
                    ('10', 'false'),
                    ('0', 'true'),
                    ('1221', 'true'),
                ]
            },
            {
                'title': 'Valid Parentheses',
                'description': '''Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

**Example 1:**
Input: s = "()"
Output: true

**Example 2:**
Input: s = "()[]{}"
Output: true

**Example 3:**
Input: s = "(]"
Output: false

**Example 4:**
Input: s = "([)]"
Output: false

**Example 5:**
Input: s = "{[]}"
Output: true''',
                'input_format': 'A string s containing only the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\'',
                'output_format': 'Output "true" if the string is valid, "false" otherwise',
                'sample_input': '()',
                'sample_output': 'true',
                'constraints': '''• 1 ≤ s.length ≤ 10⁴
• s consists of parentheses only '()[]{}'
''',
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
                'description': '''Given an integer array nums, find the subarray with the largest sum, and return its sum.

A subarray is a contiguous non-empty sequence of elements within an array.

**Example 1:**
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

**Example 2:**
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

**Example 3:**
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

**Follow up:** If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.''',
                'input_format': '''First line: Integer n (the length of the array)
Second line: n space-separated integers representing the array nums''',
                'output_format': 'A single integer representing the maximum sum of any subarray',
                'sample_input': '9\n-2 1 -3 4 -1 2 1 -5 4',
                'sample_output': '6',
                'constraints': '''• 1 ≤ nums.length ≤ 10⁵
• -10⁴ ≤ nums[i] ≤ 10⁴''',
                'difficulty': 'medium',
                'test_cases': [
                    ('9\n-2 1 -3 4 -1 2 1 -5 4', '6'),
                    ('1\n1', '1'),
                    ('5\n5 4 -1 7 8', '23'),
                    ('3\n-2 -1 -3', '-1'),
                ]
            },
            {
                'title': 'Longest Common Subsequence',
                'description': '''Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both strings.

**Example 1:**
Input: text1 = "abcde", text2 = "ace" 
Output: 3  
Explanation: The longest common subsequence is "ace" and its length is 3.

**Example 2:**
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

**Example 3:**
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.''',
                'input_format': '''First line: String text1
Second line: String text2''',
                'output_format': 'A single integer representing the length of the longest common subsequence',
                'sample_input': 'abcde\nace',
                'sample_output': '3',
                'constraints': '''• 1 ≤ text1.length, text2.length ≤ 1000
• text1 and text2 consist of only lowercase English characters''',
                'difficulty': 'medium',
                'test_cases': [
                    ('abcde\nace', '3'),
                    ('abc\nabc', '3'),
                    ('abc\ndef', '0'),
                    ('ezupkr\nubmrapg', '2'),
                ]
            },
            {
                'title': 'Climbing Stairs',
                'description': '''You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

**Example 1:**
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

**Example 2:**
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

**Note:** This is essentially a Fibonacci sequence problem.''',
                'input_format': 'A single integer n representing the number of steps',
                'output_format': 'A single integer representing the number of distinct ways to climb n steps',
                'sample_input': '3',
                'sample_output': '3',
                'constraints': '''• 1 ≤ n ≤ 45''',
                'difficulty': 'easy',
                'test_cases': [
                    ('2', '2'),
                    ('3', '3'),
                    ('4', '5'),
                    ('5', '8'),
                    ('1', '1'),
                ]
            },
            {
                'title': 'Merge Two Sorted Lists',
                'description': '''You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

**Example 1:**
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

**Example 2:**
Input: list1 = [], list2 = []
Output: []

**Example 3:**
Input: list1 = [], list2 = [0]
Output: [0]

**Note:** For this problem, represent linked lists as arrays for simplicity.''',
                'input_format': '''First line: Space-separated integers for list1 (empty line if no elements)
Second line: Space-separated integers for list2 (empty line if no elements)''',
                'output_format': 'Space-separated integers representing the merged sorted list (empty if both lists are empty)',
                'sample_input': '1 2 4\n1 3 4',
                'sample_output': '1 1 2 3 4 4',
                'constraints': '''• The number of nodes in both lists is in the range [0, 50]
• -100 ≤ Node.val ≤ 100
• Both list1 and list2 are sorted in non-decreasing order''',
                'difficulty': 'easy',
                'test_cases': [
                    ('1 2 4\n1 3 4', '1 1 2 3 4 4'),
                    ('\n', ''),
                    ('\n0', '0'),
                    ('1\n2 3 4', '1 2 3 4'),
                ]
            },
            {
                'title': 'Search in Rotated Sorted Array',
                'description': '''There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 ≤ k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

**Example 1:**
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

**Example 2:**
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

**Example 3:**
Input: nums = [1], target = 0
Output: -1''',
                'input_format': '''First line: Space-separated integers representing the rotated sorted array nums
Second line: Integer target''',
                'output_format': 'Index of target in the array (0-indexed), or -1 if not found',
                'sample_input': '4 5 6 7 0 1 2\n0',
                'sample_output': '4',
                'constraints': '''• 1 ≤ nums.length ≤ 5000
• -10⁴ ≤ nums[i] ≤ 10⁴
• All values of nums are unique
• nums is an ascending array that is possibly rotated
• -10⁴ ≤ target ≤ 10⁴''',
                'difficulty': 'medium',
                'test_cases': [
                    ('4 5 6 7 0 1 2\n0', '4'),
                    ('4 5 6 7 0 1 2\n3', '-1'),
                    ('1\n0', '-1'),
                    ('1\n1', '0'),
                ]
            },
            {
                'title': 'Longest Palindromic Substring',
                'description': '''Given a string s, return the longest palindromic substring in s.

A string is palindromic if it reads the same forward and backward.

**Example 1:**
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

**Example 2:**
Input: s = "cbbd"
Output: "bb"

**Example 3:**
Input: s = "a"
Output: "a"

**Example 4:**
Input: s = "ac"
Output: "a"

**Note:** There can be multiple valid answers. Return any one of them.''',
                'input_format': 'A single string s',
                'output_format': 'The longest palindromic substring',
                'sample_input': 'babad',
                'sample_output': 'bab',
                'constraints': '''• 1 ≤ s.length ≤ 1000
• s consist of only digits and English letters''',
                'difficulty': 'medium',
                'test_cases': [
                    ('babad', 'bab'),
                    ('cbbd', 'bb'),
                    ('a', 'a'),
                    ('ac', 'a'),
                    ('racecar', 'racecar'),
                ]
            },
            {
                'title': 'Best Time to Buy and Sell Stock',
                'description': '''You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

**Example 1:**
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

**Example 2:**
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.''',
                'input_format': '''First line: Integer n (number of days)
Second line: n space-separated integers representing stock prices''',
                'output_format': 'Maximum profit that can be achieved',
                'sample_input': '6\n7 1 5 3 6 4',
                'sample_output': '5',
                'constraints': '''• 1 ≤ prices.length ≤ 10⁵
• 0 ≤ prices[i] ≤ 10⁴''',
                'difficulty': 'easy',
                'test_cases': [
                    ('6\n7 1 5 3 6 4', '5'),
                    ('5\n7 6 4 3 1', '0'),
                    ('2\n1 2', '1'),
                    ('1\n1', '0'),
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
                    is_sample=(i == 0)  # First test case is always sample (visible to users)
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
