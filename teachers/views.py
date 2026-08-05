from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, Department, ResearchField
from projects.models import Project

@login_required
def edit_teacher_profile(request):
    try:
        teacher = Teacher.objects.get(id=request.user.id)
    except Teacher.DoesNotExist:
        messages.error(request, "Access Denied. You do not have a faculty profile.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        designation = request.POST.get('designation')
        room_no = request.POST.get('room_no')
        bio = request.POST.get('bio')
        selected_interests = request.POST.getlist('interests')
        
        # Save core fields
        request.user.first_name = f_name
        request.user.last_name = l_name
        request.user.save()
        
        # Save profile fields
        teacher.designation = designation
        teacher.room_no = room_no
        teacher.bio = bio
        teacher.save()
        
        # Save Many-to-Many research interests
        teacher.interests.clear()
        if selected_interests:
            teacher.interests.add(*selected_interests)
            
        messages.success(request, "Your faculty supervisor profile was successfully saved!")
        return redirect('dashboard')
        
    all_fields = ResearchField.objects.all().order_by('name')
    return render(request, 'teachers/edit_profile.html', {
        'teacher': teacher,
        'all_fields': all_fields
    })

@login_required
def browse_teachers(request):
    # Retrieve query filters
    search_query = request.GET.get('search', '')
    selected_dept = request.GET.get('dept', '')
    selected_interest = request.GET.get('interest', '')
    
    # Filter only approved teachers (unapproved shouldn't show in standard searches!)
    teachers_list = Teacher.objects.filter(is_approved=True)
    
    if search_query:
        teachers_list = teachers_list.filter(
            user__first_name__icontains=search_query
        ) | teachers_list.filter(
            user__last_name__icontains=search_query
        )
        
    if selected_dept:
        teachers_list = teachers_list.filter(dept_id=int(selected_dept))
        
    if selected_interest:
        teachers_list = teachers_list.filter(interests__id=int(selected_interest))
        
    departments = Department.objects.all().order_by('code')
    research_fields = ResearchField.objects.all().order_by('name')
    
    return render(request, 'students/browse_teachers.html', {
        'teachers': teachers_list.distinct(),
        'departments': departments,
        'research_fields': research_fields,
        'search_query': search_query,
        'selected_dept': selected_dept,
        'selected_interest': selected_interest
    })

@login_required
def view_teacher_profile(request, teacher_id):
    # Fetch supervisor
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        messages.error(request, "Supervisor profile not found.")
        return redirect('browse_teachers')
        
    # Fetch open projects listed by this supervisor
    projects = Project.objects.filter(teacher=teacher, status='Open').order_by('-created_at')
    
    return render(request, 'teachers/view_profile.html', {
        'teacher': teacher,
        'projects': projects
    })
