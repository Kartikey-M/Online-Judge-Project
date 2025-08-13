"""
Quick verification script to check production database status
Run this after deployment to verify problems are populated
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
django.setup()

def check_production_status():
    """Check if production database has been properly populated"""
    
    print("🔍 Code Matrix Production Database Check")
    print("=" * 50)
    
    try:
        from problems.models import Problem, TestCase
        from submissions.models import Submission
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # Check problems
        total_problems = Problem.objects.count()
        active_problems = Problem.objects.filter(is_active=True).count()
        
        print(f"📚 Problems:")
        print(f"   Total: {total_problems}")
        print(f"   Active: {active_problems}")
        
        if total_problems > 0:
            print(f"   By Difficulty:")
            for difficulty in ['easy', 'medium', 'hard']:
                count = Problem.objects.filter(difficulty=difficulty).count()
                print(f"     {difficulty.title()}: {count}")
            
            print(f"\n   Sample Problems:")
            for problem in Problem.objects.all()[:5]:
                test_cases = problem.test_cases.count()
                print(f"     - {problem.title} ({problem.difficulty}) - {test_cases} test cases")
        
        # Check test cases
        total_test_cases = TestCase.objects.count()
        sample_test_cases = TestCase.objects.filter(is_sample=True).count()
        
        print(f"\n🧪 Test Cases:")
        print(f"   Total: {total_test_cases}")
        print(f"   Sample (visible): {sample_test_cases}")
        print(f"   Hidden: {total_test_cases - sample_test_cases}")
        
        # Check users
        total_users = User.objects.count()
        admin_users = User.objects.filter(is_superuser=True).count()
        
        print(f"\n👥 Users:")
        print(f"   Total: {total_users}")
        print(f"   Admins: {admin_users}")
        
        # Check submissions
        total_submissions = Submission.objects.count()
        
        print(f"\n📝 Submissions:")
        print(f"   Total: {total_submissions}")
        
        # Overall status
        print("\n" + "=" * 50)
        
        if total_problems >= 5 and total_test_cases >= 10:
            print("✅ PRODUCTION DATABASE IS PROPERLY POPULATED!")
            print("🚀 Code Matrix is ready for users!")
            return True
        elif total_problems > 0:
            print("⚠️  Database has some problems but may need more content")
            print("💡 Consider running: python manage.py populate_problems")
            return True
        else:
            print("❌ PRODUCTION DATABASE IS EMPTY!")
            print("🔧 Run: python manage.py populate_problems")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


if __name__ == "__main__":
    success = check_production_status()
    
    print("\n📋 NEXT STEPS:")
    if success:
        print("1. Visit the admin panel to see problems")
        print("2. Check /problems/ page for user-facing problem list")
        print("3. Test AI assistant functionality")
        print("4. Try submitting solutions")
    else:
        print("1. Run: python manage.py populate_problems")
        print("2. Check deployment logs on Render.com")
        print("3. Verify build.sh is executing properly")
    
    print(f"\n🌐 Admin Panel: https://code-matrix-0ya4.onrender.com/admin/")
    print(f"🎯 Problems Page: https://code-matrix-0ya4.onrender.com/problems/")
    
    sys.exit(0 if success else 1)
