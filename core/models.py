from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    USER_TYPES = (
        ('lawyer', 'Lawyer'),
        ('judge', 'Judge'),
        ('viewer', 'Viewer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(choices=USER_TYPES, max_length=10)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class BailApplication(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bail_applications')
    client_name = models.CharField(max_length=200)
    case_number = models.CharField(max_length=100)
    incident = models.ForeignKey(Incident, on_delete=models.SET_NULL, null=True, blank=True, related_name='bail_applications')
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Required document uploads (all PDF only)
    bail_application_form = models.FileField(upload_to='bail_documents/application_forms/', null=True, blank=True)
    fir_copy = models.FileField(upload_to='bail_documents/fir_copies/', null=True, blank=True)
    proof_of_address = models.FileField(upload_to='bail_documents/address_proofs/', null=True, blank=True)
    proof_of_identity = models.FileField(upload_to='bail_documents/identity_proofs/', null=True, blank=True)
    affidavit_of_support = models.FileField(upload_to='bail_documents/affidavits/', null=True, blank=True)
    character_reference = models.FileField(upload_to='bail_documents/character_references/', null=True, blank=True)
    criminal_history = models.FileField(upload_to='bail_documents/criminal_history/', null=True, blank=True)
    
    # Additional fields for case details
    charges = models.TextField(blank=True)
    bail_amount_requested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    court_name = models.CharField(max_length=200, blank=True)
    judge_assigned = models.CharField(max_length=200, blank=True)
    hearing_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Bail Application for {self.client_name} - {self.case_number}"
    
    def is_complete(self):
        """Check if all required documents have been uploaded"""
        required_docs = [
            self.bail_application_form,
            self.fir_copy,
            self.proof_of_address,
            self.proof_of_identity,
            self.affidavit_of_support,
            self.character_reference
        ]
        return all(required_docs)

class JudgeDecision(models.Model):
    """Model to track judge decisions on bail applications"""
    application = models.OneToOneField(BailApplication, on_delete=models.CASCADE, related_name='judge_decision')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decisions')
    decision = models.CharField(max_length=20, choices=BailApplication.STATUS_CHOICES[3:5]) # 'approved' or 'rejected'
    bail_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True, help_text="Judge's comments on the decision")
    decision_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Decision for {self.application.client_name} - {self.get_decision_display()}"
    
    def save(self, *args, **kwargs):
        """Override save to update the status of the linked application"""
        super().save(*args, **kwargs)
        
        # Update application status
        self.application.status = self.decision
        self.application.save()