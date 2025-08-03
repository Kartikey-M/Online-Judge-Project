from django.db import models
from django.contrib.auth import get_user_model
from problems.models import Problem

User = get_user_model()


class Submission(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python 3'),
        ('cpp', 'C++'),
        ('c', 'C'),
        ('java', 'Java'),
    ]
    
    VERDICT_CHOICES = [
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'),
        ('MLE', 'Memory Limit Exceeded'),
        ('CE', 'Compilation Error'),
        ('RE', 'Runtime Error'),
        ('RTE', 'Runtime Error'),
        ('OLE', 'Output Limit Exceeded'),
        ('IE', 'Internal Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    source_code = models.TextField()
    verdict = models.CharField(max_length=3, choices=VERDICT_CHOICES, default='PE')
    execution_time = models.PositiveIntegerField(null=True, blank=True)  # in milliseconds
    memory_used = models.PositiveIntegerField(null=True, blank=True)  # in KB
    compilation_error = models.TextField(blank=True)
    runtime_error = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    judged_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.verdict}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submissions:detail', kwargs={'pk': self.pk})
    
    @property
    def is_accepted(self):
        return self.verdict == 'AC'
    
    @property
    def verdict_display(self):
        return dict(self.VERDICT_CHOICES).get(self.verdict, self.verdict)


class TestCaseResult(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='test_results')
    test_case_number = models.PositiveIntegerField()
    passed = models.BooleanField(default=False)
    execution_time = models.PositiveIntegerField(null=True, blank=True)  # in milliseconds
    memory_used = models.PositiveIntegerField(null=True, blank=True)  # in KB
    error_message = models.TextField(blank=True)
    
    def __str__(self):
        return f"Test case {self.test_case_number} - {'Passed' if self.passed else 'Failed'}"
