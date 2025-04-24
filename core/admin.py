from django.contrib import admin
from .models import Incident, UserProfile, BailApplication, JudgeDecision

admin.site.register(Incident)
admin.site.register(UserProfile)

@admin.register(BailApplication)
class BailApplicationAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'case_number', 'lawyer', 'status', 'date_created')
    list_filter = ('status', 'date_created')
    search_fields = ('client_name', 'case_number', 'lawyer__username')
    readonly_fields = ('date_created', 'updated_at')

@admin.register(JudgeDecision)
class JudgeDecisionAdmin(admin.ModelAdmin):
    list_display = ('application', 'judge', 'decision', 'decision_date')
    list_filter = ('decision', 'decision_date')
    search_fields = ('application__client_name', 'application__case_number', 'judge__username')
