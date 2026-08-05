from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection

from teachers.models import Teacher, Department, ResearchField
from students.models import Student, Skill
from projects.models import Project, Application

@login_required
def dashboard_router_view(request):
    # Determine user role from session
    role = request.session.get('user_role')
    
    if not role:
        # Fallback in case session was cleared but user is still authenticated
        if request.user.is_superuser:
            role = 'admin'
        elif Teacher.objects.filter(id=request.user.id).exists():
            role = 'teacher'
        elif Student.objects.filter(id=request.user.id).exists():
            role = 'student'
        else:
            role = 'student'
        request.session['user_role'] = role
        
    # Routing depending on role
    if role == 'admin' or request.user.is_superuser:
        return admin_dashboard(request)
    elif role == 'teacher':
        return teacher_dashboard(request)
    else:
        return student_dashboard(request)

def student_dashboard(request):
    student = get_object_or_404(Student, id=request.user.id)
    applications = Application.objects.filter(student=student).order_by('-created_at')
    
    # Calculate stats
    stats = {
        'total_applications': applications.count(),
        'accepted_applications': applications.filter(status='Accepted').count(),
        'pending_applications': applications.filter(status='Pending').count(),
        'rejected_applications': applications.filter(status='Rejected').count(),
    }
    
    # Fetch active/accepted supervisor list
    accepted_list = applications.filter(status='Accepted')
    
    return render(request, 'dashboard/student_dashboard.html', {
        'student': student,
        'applications': applications,
        'stats': stats,
        'accepted_list': accepted_list
    })

def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, id=request.user.id)
    projects = Project.objects.filter(teacher=teacher).order_by('-created_at')
    
    # Applications sent to this teacher
    all_apps = Application.objects.filter(teacher=teacher).order_by('-created_at')
    pending_applications = all_apps.filter(status='Pending')
    supervised_students = all_apps.filter(status='Accepted')
    
    stats = {
        'total_projects': projects.count(),
        'pending_count': pending_applications.count(),
        'accepted_count': supervised_students.count()
    }
    
    return render(request, 'dashboard/teacher_dashboard.html', {
        'teacher': teacher,
        'projects': projects,
        'pending_applications': pending_applications,
        'supervised_students': supervised_students,
        'stats': stats
    })

def admin_dashboard(request):
    # Admin stats using Django aggregation
    stats = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'approved_teachers': Teacher.objects.filter(is_approved=True).count(),
        'pending_teachers': Teacher.objects.filter(is_approved=False).count(),
        'total_projects': Project.objects.count(),
        'total_applications': Application.objects.count(),
    }
    
    # List of teachers pending approval
    pending_list = Teacher.objects.filter(is_approved=False).order_by('-created_at')
    
    # Fetch recent registrations (latest 5 users)
    recent_registrations = User.objects.all().order_by('-date_joined')[:5]
    
    # Fetch teacher workload using direct query on the MySQL database VIEW!
    workload_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT first_name, last_name, dept_name, accepted_supervisions FROM view_teacher_workload ORDER BY accepted_supervisions DESC")
            columns = [col[0] for col in cursor.description]
            workload_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        messages.error(request, f"Could not load workload view: {str(e)}")
        
    return render(request, 'dashboard/admin_dashboard.html', {
        'stats': stats,
        'pending_list': pending_list,
        'recent_registrations': recent_registrations,
        'workload_data': workload_data
    })

@login_required
def approve_teacher_profile_view(request, teacher_id):
    # Ensure only administrators can perform this action
    if not request.user.is_superuser and request.session.get('user_role') != 'admin':
        messages.error(request, "Access Denied. Only administrators can approve profiles.")
        return redirect('dashboard')
        
    # Execute Database Stored Procedure to Approve teacher!
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_approve_teacher', [teacher_id])
        messages.success(request, f"Supervisor profile (ID: {teacher_id}) was successfully approved via DB stored procedure!")
    except Exception as e:
        messages.error(request, f"Error calling database procedure: {str(e)}")
        
    return redirect('dashboard')

@login_required
def edit_my_profile_view(request):
    role = request.session.get('user_role')
    if role == 'teacher':
        return redirect('teacher_profile_edit')
    elif role == 'student':
        return redirect('student_profile_edit')
    else:
        messages.info(request, "Administrators do not require student or faculty profiles.")
        return redirect('dashboard')
