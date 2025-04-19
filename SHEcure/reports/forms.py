from django import forms
from .models import HarassmentReport, Comment

class HarassmentReportForm(forms.ModelForm):
    class Meta:
        model = HarassmentReport
        fields = ['location', 'time', 'date', 'harassment_type', 'description', 'reported_by']
        widgets = {
            'time': forms.TimeInput(attrs={'placeholder': 'e.g., 10:30:00', 'type': 'time'}),
            'date': forms.DateInput(attrs={'placeholder': 'e.g., 2025-01-01', 'type': 'date'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment here...'}),
        }