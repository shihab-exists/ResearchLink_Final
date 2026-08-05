from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from teachers.models import Department, Teacher
from students.models import Student

def login_view(request):
    # If already authenticated, go to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        
        user = authenticate(request, username=u_name, password=p_word)
        
        if user is not None:
            login(request, user)
            
            # Determine user role and store in session
            if user.is_superuser:
                request.session['user_role'] = 'admin'
            elif Teacher.objects.filter(id=user.id).exists():
                request.session['user_role'] = 'teacher'
            elif Student.objects.filter(id=user.id).exists():
                request.session['user_role'] = 'student'
            else:
                # Default safety fallback
                request.session['user_role'] = 'student'
                
            messages.success(request, f"Successfully logged in as {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        role = request.POST.get('role')
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        p_word = request.POST.get('password')
        dept_id = request.POST.get('dept')
        
        # Validations
        if User.objects.filter(username=u_name).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please choose another.")
            return redirect('register')
            
        # Create Core Auth User
        user = User.objects.create_user(username=u_name, email=email, password=p_word, first_name=f_name, last_name=l_name)
        
        # Get Department instance
        dept = None
        if dept_id:
            dept = Department.objects.get(id=int(dept_id))
            
        if role == 'student':
            roll_no = request.POST.get('roll_no')
            cgpa = request.POST.get('cgpa')
            
            # Create Student Profile
            Student.objects.create(
                user=user,
                dept=dept,
                roll_no=roll_no,
                cgpa=cgpa,
                bio="New student researcher. Looking for opportunities!"
            )
            request.session['user_role'] = 'student'
            
        elif role == 'teacher':
            designation = request.POST.get('designation')
            room_no = request.POST.get('room_no')
            
            # Create Teacher Profile (requires admin approval)
            Teacher.objects.create(
                user=user,
                dept=dept,
                designation=designation,
                room_no=room_no,
                is_approved=False, # Must be approved by Admin in dashboard
                bio="Experienced faculty member looking forward to reviewing student research pitches."
            )
            request.session['user_role'] = 'teacher'
            
        # Log the user in directly after registration
        login(request, user)
        messages.success(request, f"Registration successful! Welcome to ResearchLink.")
        return redirect('dashboard')
        
    departments = Department.objects.all().order_by('code')
    return render(request, 'accounts/register.html', {'departments': departments})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully. See you again!")
    return redirect('login')
