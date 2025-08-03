from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial language to Python if not specified
        if not self.initial.get('language'):
            self.fields['language'].initial = 'python'
        # Make the language field more intuitive
        self.fields['language'].widget.attrs.update({
            'class': 'form-select',
            'onchange': 'console.log("Language dropdown changed:", this.value);'
        })
        self.fields['source_code'].widget.attrs.update({
            'placeholder': '# Your code will appear here based on selected language...',
            'class': 'form-control code-editor'
        })
    
    class Meta:
        model = Submission
        fields = ['language', 'source_code']
        widgets = {
            'source_code': forms.Textarea(attrs={
                'rows': 20,
                'cols': 80,
                'class': 'form-control code-editor',
            }),
            'language': forms.Select()
        }
        
    def clean_source_code(self):
        source_code = self.cleaned_data.get('source_code')
        if not source_code or source_code.strip() == '':
            raise forms.ValidationError('Source code cannot be empty.')
        if len(source_code.strip()) < 10:
            raise forms.ValidationError('Source code is too short. Please provide a meaningful solution.')
        return source_code
