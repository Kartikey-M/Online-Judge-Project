from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Statistics
    problems_solved = models.PositiveIntegerField(default=0)
    total_submissions = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.username
    
    def update_statistics(self):
        """Update user statistics"""
        from submissions.models import Submission
        self.total_submissions = Submission.objects.filter(user=self).count()
        self.problems_solved = Submission.objects.filter(
            user=self, 
            verdict='AC'
        ).values('problem').distinct().count()
        self.save()
