from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['language', 'source_code']
        widgets = {
            'source_code': forms.Textarea(attrs={
                'rows': 20,
                'cols': 80,
                'class': 'form-control code-editor',
                'placeholder': 'Write your code here...'
            }),
            'language': forms.Select(attrs={
                'class': 'form-control'
            })
        }
