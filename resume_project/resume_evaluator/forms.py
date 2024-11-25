from django import forms
from .models import ResumeEvaluation

class ResumeEvaluationForm(forms.ModelForm):
    class Meta:
        model = ResumeEvaluation
        fields = ['resume', 'job_description']
        widgets = {
            'job_description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500',
                'placeholder': 'Enter the job description here...',
                'rows': 8,
                'style': 'resize: vertical; min-height: 200px;'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': '.pdf'
            })
        }