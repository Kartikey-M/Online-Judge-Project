#!/usr/bin/env python
"""
Test script to verify Online Judge functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
django.setup()

from accounts.models import User
from problems.models import Problem
from submissions.models import Submission

def test_system():
    print("=== ONLINE JUDGE SYSTEM VERIFICATION ===\n")
    
    # Test 1: Check users
    print("1. User Authentication:")
    users = User.objects.all()
    print(f"   Total users: {users.count()}")
    for user in users:
        print(f"   - {user.username} (superuser: {user.is_superuser})")
    
    # Test 2: Check problems
    print("\n2. Problems:")
    problems = Problem.objects.filter(is_active=True)
    print(f"   Active problems: {problems.count()}")
    for problem in problems[:3]:
        print(f"   - {problem.title} (slug: {problem.slug})")
    
    # Test 3: Check submissions
    print("\n3. Submissions:")
    submissions = Submission.objects.all()
    print(f"   Total submissions: {submissions.count()}")
    
    # Test 4: Create test submission
    print("\n4. Testing Submission Creation:")
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        test_problem = Problem.objects.filter(is_active=True).first()
        
        if admin_user and test_problem:
            # Create test submission
            test_submission = Submission.objects.create(
                user=admin_user,
                problem=test_problem,
                language='python',
                source_code='print("Hello, World!")',
                verdict='AC'
            )
            print(f"   ✅ Test submission created: ID {test_submission.id}")
            print(f"   User: {test_submission.user.username}")
            print(f"   Problem: {test_submission.problem.title}")
            print(f"   Language: {test_submission.language}")
            print(f"   Verdict: {test_submission.verdict}")
            
            # Update user statistics
            admin_user.update_statistics()
            print(f"   ✅ User stats updated - Problems solved: {admin_user.problems_solved}")
            
        else:
            print("   ❌ Missing admin user or test problem")
    
    except Exception as e:
        print(f"   ❌ Error creating test submission: {e}")
    
    # Test 5: Verify templates
    print("\n5. Template Status:")
    template_paths = [
        'templates/accounts/profile.html',
        'templates/accounts/edit_profile.html',
        'templates/accounts/login.html',
        'templates/problems/detail.html',
        'templates/submissions/detail.html'
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            print(f"   ✅ {template_path}")
        else:
            print(f"   ❌ {template_path} - MISSING")
    
    print("\n=== VERIFICATION COMPLETE ===")

if __name__ == '__main__':
    test_system()
