from django.contrib import admin
from .models import Submission, TestCaseResult


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'problem', 'language', 'verdict', 'submitted_at']
    list_filter = ['language', 'verdict', 'submitted_at']
    search_fields = ['user__username', 'problem__title']
    readonly_fields = ['submitted_at', 'judged_at']
    date_hierarchy = 'submitted_at'


@admin.register(TestCaseResult)
class TestCaseResultAdmin(admin.ModelAdmin):
    list_display = ['submission', 'test_case_number', 'passed', 'execution_time']
    list_filter = ['passed']
    search_fields = ['submission__user__username', 'submission__problem__title']
