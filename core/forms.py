from django import forms
from .models import UserProfile, Incident, BailApplication, JudgeDecision
import os

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

def validate_pdf_file(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise forms.ValidationError('Only PDF files are allowed.')
    return value

class BailApplicationForm(forms.ModelForm):
    bail_application_form = forms.FileField(
        validators=[validate_pdf_file],
        help_text='PDF format only. Upload the bail application form drafted for this specific case.',
        required=False
    )
    fir_copy = forms.FileField(
        validators=[validate_pdf_file],
        help_text='PDF format only. Upload a copy of the FIR obtained from the police.',
        required=False
    )
    proof_of_address = forms.FileField(
        validators=[validate_pdf_file],
        help_text='PDF format only. Upload a copy of proof of address document.',
        required=False
    )
    proof_of_identity = forms.FileField(
        validators=[validate_pdf_file],
        help_text='PDF format only. Upload a copy of government-issued ID.',
        required=False
    )
    affidavit_of_support = forms.FileField(
        validators=[validate_pdf_file],
        help_text='PDF format only. Upload the affidavit of support following legal requirements.',
        required=False
    )
    character_reference = forms.FileField(
        validators=[validate_pdf_file],
        help_text='PDF format only. Upload a character reference letter from a third party.',
        required=False
    )
    criminal_history = forms.FileField(
        validators=[validate_pdf_file],
        help_text='PDF format only. Upload criminal history documentation if any.',
        required=False
    )
    
    class Meta:
        model = BailApplication
        fields = [
            'client_name', 'case_number', 'incident', 'charges', 
            'bail_amount_requested', 'court_name', 'hearing_date',
            'bail_application_form', 'fir_copy', 'proof_of_address', 
            'proof_of_identity', 'affidavit_of_support', 'character_reference', 
            'criminal_history'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'case_number': forms.TextInput(attrs={'class': 'form-control'}),
            'incident': forms.Select(attrs={'class': 'form-control'}),
            'charges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bail_amount_requested': forms.NumberInput(attrs={'class': 'form-control'}),
            'court_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hearing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class JudgeDecisionForm(forms.ModelForm):
    """Form for judges to make decisions on bail applications"""
    DECISION_CHOICES = [
        ('approved', 'Approve Bail'),
        ('rejected', 'Reject Bail'),
    ]
    
    decision = forms.ChoiceField(
        choices=DECISION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'decision-radio'}),
        required=True
    )
    
    bail_amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Required only if bail is approved"
    )
    
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
    
    class Meta:
        model = JudgeDecision
        fields = ['decision', 'bail_amount', 'comments']
        
    def clean(self):
        cleaned_data = super().clean()
        decision = cleaned_data.get('decision')
        bail_amount = cleaned_data.get('bail_amount')
        
        if decision == 'approved' and not bail_amount:
            self.add_error('bail_amount', 'Bail amount is required when approving bail')
            
        return cleaned_data