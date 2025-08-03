#!/usr/bin/env python
"""
Test script for Gemini AI integration
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
django.setup()

from ai_assistant.gemini_service import gemini_service

def test_gemini_service():
    """Test the Gemini service with sample data."""
    print("Testing Gemini AI Integration...")
    print("=" * 50)
    
    # Test 1: Problem Hint
    print("\n1. Testing Problem Hint Generation:")
    print("-" * 30)
    
    problem_title = "Two Sum"
    problem_description = """Given an array of integers nums and an integer target, 
    return indices of the two numbers such that they add up to target.
    
    You may assume that each input would have exactly one solution, 
    and you may not use the same element twice."""
    
    hint = gemini_service.generate_problem_hint(
        problem_title=problem_title,
        problem_description=problem_description,
        difficulty="easy"
    )
    
    if hint:
        print(f"✅ Hint generated successfully:")
        print(f"'{hint}'")
    else:
        print("❌ Failed to generate hint")
    
    # Test 2: Wrong Answer Analysis
    print("\n2. Testing Wrong Answer Analysis:")
    print("-" * 30)
    
    sample_code = """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Test
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))
"""
    
    analysis = gemini_service.analyze_wrong_answer(
        problem_title=problem_title,
        problem_description=problem_description,
        user_code=sample_code,
        language="python",
        expected_output="[0, 1]",
        actual_output="[0, 1]"
    )
    
    if analysis:
        print(f"✅ Analysis generated successfully:")
        print(f"'{analysis}'")
    else:
        print("❌ Failed to generate analysis")
    
    # Test 3: Runtime Error Analysis
    print("\n3. Testing Runtime Error Analysis:")
    print("-" * 30)
    
    buggy_code = """
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 0)
print(result)
"""
    
    runtime_analysis = gemini_service.analyze_runtime_error(
        problem_title="Division Problem",
        user_code=buggy_code,
        language="python",
        error_message="ZeroDivisionError: division by zero"
    )
    
    if runtime_analysis:
        print(f"✅ Runtime error analysis generated successfully:")
        print(f"'{runtime_analysis}'")
    else:
        print("❌ Failed to generate runtime error analysis")
    
    print("\n" + "=" * 50)
    print("Gemini AI Integration Test Complete!")

if __name__ == "__main__":
    test_gemini_service()
