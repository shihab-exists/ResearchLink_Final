from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Skill
from django.contrib.auth.models import User

@login_required
def edit_student_profile(request):
    # Ensure current user is indeed a student
    try:
        student = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        messages.error(request, "Access Denied. You do not have a student profile.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        # Get standard inputs
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        roll_no = request.POST.get('roll_no')
        cgpa = request.POST.get('cgpa')
        cv_url = request.POST.get('cv_url')
        bio = request.POST.get('bio')
        selected_skills = request.POST.getlist('skills') # List of skill IDs
        
        # Save Auth User fields
        request.user.first_name = f_name
        request.user.last_name = l_name
        request.user.save()
        
        # Save Profile fields
        student.roll_no = roll_no
        student.cgpa = cgpa
        student.cv_url = cv_url
        student.bio = bio
        student.save()
        
        # Update skills association (Many-to-Many)
        student.skills.clear()
        if selected_skills:
            student.skills.add(*selected_skills)
            
        messages.success(request, "Your student profile has been updated successfully!")
        return redirect('dashboard')
        
    all_skills = Skill.objects.all().order_by('name')
    return render(request, 'students/edit_profile.html', {
        'student': student,
        'all_skills': all_skills
    })

@login_required
def student_applications_view(request):
    try:
        student = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        messages.error(request, "Access Denied. You do not have a student profile.")
        return redirect('dashboard')
        
    apps = Application.objects.filter(student=student).order_by('-created_at')
    return render(request, 'students/applications.html', {
        'applications': apps
    })
