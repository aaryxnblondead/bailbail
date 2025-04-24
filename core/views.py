from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Incident, UserProfile, BailApplication, JudgeDecision
from .forms import UserProfileForm, IncidentForm, BailApplicationForm, JudgeDecisionForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def incidents(request):
    incidents = Incident.objects.all().order_by('-date_created')
    return render(request, 'incidents.html', {'incidents': incidents})

def incident_detail(request, incident_id):
    """View a single incident in detail"""
    incident = get_object_or_404(Incident, id=incident_id)
    return render(request, 'incident_detail.html', {'incident': incident})

def insights(request):
    return render(request, 'insights.html')

def register(request):
    if request.method == 'POST':
        # Your existing POST handling code
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        
        # Basic validation
        if not (username and email and password1 and password2 and user_type):
            messages.error(request, 'Please fill in all fields')
            return render(request, 'register.html')
            
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')
        
        # Create the user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            # Create user profile with selected user type
            UserProfile.objects.create(
                user=user,
                user_type=user_type
            )
            
            # Authenticate and login the user
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, f"Account successfully created! Welcome, {username}!")
                return redirect('home')  # Redirect to home page after successful registration
                
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'register.html')
    
    # For GET requests - this is the line that was likely missing
    return render(request, 'register.html')

def user_login(request, user_type):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user has the correct user_type
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.user_type == user_type:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, f"You are not registered as a {user_type}")
            except UserProfile.DoesNotExist:
                messages.error(request, "Profile does not exist")
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, f'{user_type}_login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_profile(request):
    """View and edit user profile information"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        messages.success(request, "Profile updated successfully")
        return redirect('user_profile')
    
    context = {
        'profile': profile
    }
    
    return render(request, 'user_profile.html', context)

@login_required
def add_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incidents')
    else:
        form = IncidentForm()
    
    return render(request, 'add_incident.html', {'form': form})

@login_required
def dashboard(request):
    # Show different dashboard based on user type
    try:
        user_type = request.user.userprofile.user_type
        if user_type == 'judge':
            return redirect('judge_dashboard')
        elif user_type == 'lawyer':
            return redirect('lawyer_dashboard')
    except:
        pass
        
    # Default dashboard for other user types
    return render(request, 'dashboard.html')

# Bail Application Views

def is_lawyer(user):
    """Check if the user is a lawyer"""
    try:
        return user.userprofile.user_type == 'lawyer'
    except UserProfile.DoesNotExist:
        return False

def is_judge(user):
    """Check if the user is a judge"""
    try:
        return user.userprofile.user_type == 'judge'
    except UserProfile.DoesNotExist:
        return False

@login_required
def lawyer_dashboard(request):
    """Dashboard view for lawyers"""
    if not is_lawyer(request.user):
        messages.error(request, "Only lawyers can access this dashboard")
        return redirect('home')
    
    # Get all applications for this lawyer
    applications = BailApplication.objects.filter(lawyer=request.user).order_by('-date_created')
    
    # Group by status
    draft_applications = applications.filter(status='draft')
    submitted_applications = applications.filter(status='submitted')
    under_review_applications = applications.filter(status='under_review')
    approved_applications = applications.filter(status='approved')
    rejected_applications = applications.filter(status='rejected')
    
    context = {
        'draft_applications': draft_applications,
        'submitted_applications': submitted_applications,
        'under_review_applications': under_review_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
    }
    
    return render(request, 'lawyer_dashboard.html', context)

@login_required
def bail_applications_list(request):
    """View all bail applications for a lawyer"""
    if not is_lawyer(request.user):
        messages.error(request, "Only lawyers can access bail applications")
        return redirect('home')
    
    applications = BailApplication.objects.filter(lawyer=request.user).order_by('-date_created')
    return render(request, 'bail_applications_list.html', {'applications': applications})

@login_required
def create_bail_application(request):
    """Create a new bail application"""
    if not is_lawyer(request.user):
        messages.error(request, "Only lawyers can create bail applications")
        return redirect('home')
    
    if request.method == 'POST':
        form = BailApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.lawyer = request.user
            application.save()
            messages.success(request, "Bail application created successfully")
            return redirect('bail_application_detail', application_id=application.id)
    else:
        form = BailApplicationForm()
    
    # Include reference PDFs
    return render(request, 'create_bail_application.html', {
        'form': form,
    })

@login_required
def bail_application_detail(request, application_id):
    """View a single bail application"""
    application = get_object_or_404(BailApplication, id=application_id)
    
    # Ensure only the lawyer who created it or a judge can view it
    if application.lawyer != request.user and not is_judge(request.user) and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to view this application")
    
    # Check if there's a decision for this application
    try:
        decision = JudgeDecision.objects.get(application=application)
    except JudgeDecision.DoesNotExist:
        decision = None
    
    return render(request, 'bail_application_detail.html', {
        'application': application,
        'decision': decision
    })

@login_required
def edit_bail_application(request, application_id):
    """Edit an existing bail application"""
    application = get_object_or_404(BailApplication, id=application_id)
    
    # Ensure only the lawyer who created it can edit it
    if application.lawyer != request.user:
        return HttpResponseForbidden("You don't have permission to edit this application")
    
    # Only allow editing if application is in draft status
    if application.status != 'draft':
        messages.error(request, "You cannot edit an application that has already been submitted")
        return redirect('bail_application_detail', application_id=application.id)
    
    if request.method == 'POST':
        form = BailApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Bail application updated successfully")
            return redirect('bail_application_detail', application_id=application.id)
    else:
        form = BailApplicationForm(instance=application)
    
    return render(request, 'edit_bail_application.html', {
        'form': form,
        'application': application
    })

@login_required
def submit_bail_application(request, application_id):
    """Submit a bail application for review"""
    application = get_object_or_404(BailApplication, id=application_id)
    
    # Ensure only the lawyer who created it can submit it
    if application.lawyer != request.user:
        return HttpResponseForbidden("You don't have permission to submit this application")
    
    # Verify all required documents are uploaded
    if not all([
        application.bail_application_form,
        application.fir_copy,
        application.proof_of_address,
        application.proof_of_identity,
        application.affidavit_of_support,
        application.character_reference
    ]):
        messages.error(request, "All required documents must be uploaded before submitting")
        return redirect('bail_application_detail', application_id=application.id)
    
    # Update application status
    application.status = 'submitted'
    application.save()
    
    messages.success(request, "Bail application submitted successfully for review")
    return redirect('bail_application_detail', application_id=application.id)

@login_required
def delete_bail_application(request, application_id):
    """Delete a bail application"""
    application = get_object_or_404(BailApplication, id=application_id)
    
    # Ensure only the lawyer who created it can delete it
    if application.lawyer != request.user:
        return HttpResponseForbidden("You don't have permission to delete this application")
    
    # Only allow deletion if application is in draft status
    if application.status != 'draft':
        messages.error(request, "You cannot delete an application that has already been submitted")
        return redirect('bail_application_detail', application_id=application.id)
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, "Bail application deleted successfully")
        return redirect('bail_applications_list')
    
    return render(request, 'delete_bail_application.html', {
        'application': application
    })

# Judge Views

@login_required
def judge_dashboard(request):
    """Dashboard for judges"""
    if not is_judge(request.user):
        messages.error(request, "Only judges can access this page")
        return redirect('home')
    
    # Get applications for review
    pending_applications = BailApplication.objects.filter(status__in=['submitted', 'under_review'])
    recent_decisions = JudgeDecision.objects.filter(judge=request.user).order_by('-decision_date')[:5]
    
    context = {
        'pending_applications': pending_applications,
        'recent_decisions': recent_decisions
    }
    
    return render(request, 'judge_dashboard.html', context)

@login_required
def judge_applications_list(request):
    """List all bail applications for judges to review"""
    if not is_judge(request.user):
        messages.error(request, "Only judges can access this page")
        return redirect('home')
    
    # Get all applications that are not in draft status
    applications = BailApplication.objects.exclude(status='draft').order_by('-date_created')
    
    # Group by status
    submitted_applications = applications.filter(status='submitted')
    under_review_applications = applications.filter(status='under_review')
    approved_applications = applications.filter(status='approved')
    rejected_applications = applications.filter(status='rejected')
    
    context = {
        'submitted_applications': submitted_applications,
        'under_review_applications': under_review_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications
    }
    
    return render(request, 'judge_applications_list.html', context)

@login_required
def judge_review_application(request, application_id):
    """Allow judges to review a specific application and make decisions"""
    if not is_judge(request.user):
        messages.error(request, "Only judges can access this page")
        return redirect('home')
    
    application = get_object_or_404(BailApplication, id=application_id)
    
    # If application is in submitted status, mark it as under review
    if application.status == 'submitted':
        application.status = 'under_review'
        application.save()
        messages.info(request, f"Application for {application.client_name} is now under review")
    
    # Process POST requests for decisions
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handle "mark as under review" action
        if action == 'mark_under_review':
            application.status = 'under_review'
            application.save()
            messages.success(request, f"Application for {application.client_name} is now under review")
            return redirect('judge_review_application', application_id=application.id)
        
        # Handle decision action
        elif action == 'make_decision':
            # Check if a decision already exists
            try:
                existing_decision = JudgeDecision.objects.get(application=application)
            except JudgeDecision.DoesNotExist:
                existing_decision = None
                
            form = JudgeDecisionForm(request.POST, instance=existing_decision)
            if form.is_valid():
                decision = form.save(commit=False)
                decision.application = application
                decision.judge = request.user
                decision.save()
                
                messages.success(request, f"Your decision on {application.client_name}'s application has been recorded.")
                return redirect('judge_applications_list')
            else:
                messages.error(request, "There was an error with your decision. Please check the form and try again.")
    else:
        # For GET requests
        form = JudgeDecisionForm()
    
    # Check if a decision already exists for this application
    try:
        existing_decision = JudgeDecision.objects.get(application=application)
    except JudgeDecision.DoesNotExist:
        existing_decision = None
    except Exception as e:
        # Handle database errors gracefully
        existing_decision = None
        messages.warning(request, f"Could not retrieve existing decision information. Database error: {str(e)}")
    
    # Prepare context with all necessary data
    context = {
        'application': application,
        'form': form,
        'existing_decision': existing_decision
    }
    
    return render(request, 'judge_review_application.html', context)

@login_required
def judge_decision_history(request):
    """View decision history for a judge"""
    if not is_judge(request.user):
        messages.error(request, "Only judges can access this page")
        return redirect('home')
    
    decisions = JudgeDecision.objects.filter(judge=request.user).order_by('-decision_date')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(decisions, 10)  # Show 10 decisions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'judge_decision_history.html', {'decisions': page_obj})

# Viewer Views
def is_viewer(user):
    """Check if a user is a viewer"""
    try:
        return user.userprofile.user_type == 'viewer'
    except:
        return False

@login_required
def viewer_dashboard(request):
    """Dashboard for viewers"""
    if not is_viewer(request.user):
        messages.error(request, "Only viewers can access this page")
        return redirect('home')
    
    # Get applications for viewing - ONLY if a case number is provided
    search_query = request.GET.get('search', '')
    
    # Start with an empty queryset
    applications = BailApplication.objects.none()
    total_applications = 0
    applications_submitted = 0
    applications_approved = 0
    applications_rejected = 0
    
    # Only show applications if a search query (case number) is provided
    if search_query:
        # Only search by case number - removed search by client_name
        applications = BailApplication.objects.exclude(status='draft').filter(
            case_number__icontains=search_query)
        
        # Apply status filter if provided
        status_filter = request.GET.get('status', '')
        if status_filter:
            applications = applications.filter(status=status_filter)
        
        # Apply sorting
        sort_option = request.GET.get('sort', 'date_new')
        if sort_option == 'date_old':
            applications = applications.order_by('date_created')
        elif sort_option == 'date_new':
            applications = applications.order_by('-date_created')
        elif sort_option == 'amount_high':
            applications = applications.order_by('-bail_amount_requested')
        elif sort_option == 'amount_low':
            applications = applications.order_by('bail_amount_requested')
        
        # Count by status for the stats cards
        total_applications = applications.count()
        applications_submitted = applications.filter(status__in=['submitted', 'under_review']).count()
        applications_approved = applications.filter(status='approved').count()
        applications_rejected = applications.filter(status='rejected').count()
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(applications, 10)  # Show 10 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Add lawyer names to the applications for display
    for application in page_obj:
        application.lawyer_name = application.lawyer.get_full_name() or application.lawyer.username
        if hasattr(application, 'judge_decision'):
            application.decision_date = application.judge_decision.decision_date
            application.bail_amount_granted = application.judge_decision.bail_amount
    
    context = {
        'applications': page_obj,
        'total_applications': total_applications,
        'applications_submitted': applications_submitted,
        'applications_approved': applications_approved,
        'applications_rejected': applications_rejected,
        'search_query': search_query,
    }
    
    return render(request, 'viewer_dashboard.html', context)

@login_required
def viewer_application_detail(request, application_id):
    """View a single bail application for viewers"""
    if not is_viewer(request.user):
        messages.error(request, "Only viewers can access this page")
        return redirect('home')
    
    application = get_object_or_404(BailApplication, id=application_id)
    
    # Get the case number from the URL parameter
    case_number = request.GET.get('case_number', '')
    
    # Check if the case number provided matches the application's case number
    # Only allow viewing if the correct case number is provided
    if not case_number or application.case_number != case_number:
        messages.error(request, "You must provide the correct case number to view this application")
        return redirect('viewer_dashboard')
    
    # Add lawyer name to the application
    application.lawyer_name = application.lawyer.get_full_name() or application.lawyer.username
    
    # Get decision if it exists
    try:
        decision = JudgeDecision.objects.get(application=application)
    except JudgeDecision.DoesNotExist:
        decision = None
    
    context = {
        'application': application,
        'decision': decision
    }
    
    return render(request, 'viewer_application_detail.html', context)