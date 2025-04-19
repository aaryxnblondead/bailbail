from django import forms
from .models import UserProfile, Incident

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'})
        }

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }