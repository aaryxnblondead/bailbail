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