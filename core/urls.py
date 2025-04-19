from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('incidents/', views.incidents, name='incidents'),
    path('insights/', views.insights, name='insights'),
    path('lawyer-login/', views.user_login, {'user_type': 'lawyer'}, name='lawyer_login'),
    path('judge-login/', views.user_login, {'user_type': 'judge'}, name='judge_login'),
    path('viewer-login/', views.user_login, {'user_type': 'viewer'}, name='viewer_login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-incident/', views.add_incident, name='add_incident'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]