from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Incident, UserProfile
from .forms import UserProfileForm, IncidentForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def incidents(request):
    incidents = Incident.objects.all().order_by('-date_created')
    return render(request, 'incidents.html', {'incidents': incidents})

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
            return render(request, 'core/register.html')
            
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'core/register.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'core/register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'core/register.html')
        
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
    return render(request,'dashboard.html')