from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('incidents/', views.incidents, name='incidents'),
    path('incidents/<int:incident_id>/', views.incident_detail, name='incident_detail'),
    path('insights/', views.insights, name='insights'),
    path('lawyer-login/', views.user_login, {'user_type': 'lawyer'}, name='lawyer_login'),
    path('judge-login/', views.user_login, {'user_type': 'judge'}, name='judge_login'),
    path('viewer-login/', views.user_login, {'user_type': 'viewer'}, name='viewer_login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('add-incident/', views.add_incident, name='add_incident'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Lawyer dashboard
    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    
    # Bail Application URLs for lawyers
    path('bail-applications/', views.bail_applications_list, name='bail_applications_list'),
    path('bail-applications/create/', views.create_bail_application, name='create_bail_application'),
    path('bail-applications/<int:application_id>/', views.bail_application_detail, name='bail_application_detail'),
    path('bail-applications/<int:application_id>/edit/', views.edit_bail_application, name='edit_bail_application'),
    path('bail-applications/<int:application_id>/submit/', views.submit_bail_application, name='submit_bail_application'),
    path('bail-applications/<int:application_id>/delete/', views.delete_bail_application, name='delete_bail_application'),
    
    # Judge URLs
    path('judge/dashboard/', views.judge_dashboard, name='judge_dashboard'),
    path('judge/applications/', views.judge_applications_list, name='judge_applications_list'),
    path('judge/applications/<int:application_id>/', views.judge_review_application, name='judge_review_application'),
    path('judge/decisions/', views.judge_decision_history, name='judge_decision_history'),
    
    # Viewer URLs
    path('viewer/dashboard/', views.viewer_dashboard, name='viewer_dashboard'),
    path('viewer/applications/<int:application_id>/', views.viewer_application_detail, name='viewer_application_detail'),
]