from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection, IntegrityError, utils
from .models import Project, Application
from teachers.models import Teacher
from students.models import Student

@login_required
def manage_projects_view(request):
    try:
        teacher = Teacher.objects.get(id=request.user.id)
    except Teacher.DoesNotExist:
        messages.error(request, "Access Denied. You do not have a faculty profile.")
        return redirect('dashboard')
        
    projects = Project.objects.filter(teacher=teacher).order_by('-created_at')
    return render(request, 'projects/manage_projects.html', {
        'projects': projects
    })

@login_required
def create_project_view(request):
    try:
        teacher = Teacher.objects.get(id=request.user.id)
    except Teacher.DoesNotExist:
        return redirect('dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        
        Project.objects.create(
            title=title,
            status=status,
            description=description,
            requirements=requirements,
            teacher=teacher
        )
        messages.success(request, f"New research opportunity '{title}' posted successfully!")
        return redirect('manage_projects')
        
    return render(request, 'projects/project_form.html', {'form_action': 'create'})

@login_required
def edit_project_view(request, project_id):
    try:
        teacher = Teacher.objects.get(id=request.user.id)
        project = Project.objects.get(id=project_id, teacher=teacher)
    except (Teacher.DoesNotExist, Project.DoesNotExist):
        messages.error(request, "Listing not found.")
        return redirect('manage_projects')
        
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.status = request.POST.get('status')
        project.description = request.POST.get('description')
        project.requirements = request.POST.get('requirements')
        project.save()
        
        messages.success(request, f"Opportunity '{project.title}' updated successfully!")
        return redirect('manage_projects')
        
    return render(request, 'projects/project_form.html', {
        'project': project,
        'form_action': 'edit'
    })

@login_required
def delete_project_view(request, project_id):
    try:
        teacher = Teacher.objects.get(id=request.user.id)
        project = Project.objects.get(id=project_id, teacher=teacher)
        project.delete()
        messages.success(request, "Opportunity removed successfully.")
    except (Teacher.DoesNotExist, Project.DoesNotExist):
        messages.error(request, "Action failed.")
        
    return redirect('manage_projects')

@login_required
def apply_supervision_view(request, teacher_id):
    try:
        student = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        messages.error(request, "Only students can submit supervision proposals.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        p_id_str = request.POST.get('project_id')
        message = request.POST.get('message')
        
        p_id = int(p_id_str) if p_id_str else None
        teacher = get_object_or_404(Teacher, id=teacher_id)
        project = get_object_or_404(Project, id=p_id) if p_id else None
        
        try:
            # Insert application proposal using Django ORM
            # Our custom database trigger 'trig_prevent_multiple_supervisors_insert'
            # will automatically execute at the database level!
            Application.objects.create(
                project=project,
                student=student,
                teacher=teacher,
                message=message,
                status='Pending'
            )
            messages.success(request, "Your supervision proposal was successfully submitted!")
            
        except (utils.InternalError, utils.OperationalError, IntegrityError) as e:
            # Capture database trigger error signals
            err_msg = str(e)
            if "already has an assigned" in err_msg:
                messages.error(request, "Application failed: You already have an accepted thesis supervisor.")
            else:
                messages.error(request, f"Database constraint error: {err_msg}")
        except Exception as e:
            messages.error(request, f"Submission failed: {str(e)}")
            
    return redirect('view_teacher_profile', teacher_id=teacher_id)

@login_required
def respond_application_view(request, application_id, status):
    try:
        teacher = Teacher.objects.get(id=request.user.id)
        app = Application.objects.get(id=application_id, teacher=teacher)
    except (Teacher.DoesNotExist, Application.DoesNotExist):
        messages.error(request, "Proposal request not found.")
        return redirect('dashboard')
        
    if status in ['Accepted', 'Rejected']:
        try:
            app.status = status
            app.save()
            messages.success(request, f"Proposal has been marked as {status}!")
        except (utils.InternalError, utils.OperationalError, IntegrityError) as e:
            # Capture database trigger error signals (e.g., student already accepted elsewhere!)
            err_msg = str(e)
            if "already has an assigned" in err_msg:
                messages.error(request, "Action failed: This student already has an accepted supervisor in another track.")
            else:
                messages.error(request, f"Database trigger validation failed: {err_msg}")
        except Exception as e:
            messages.error(request, f"Action failed: {str(e)}")
    else:
        messages.error(request, "Invalid response status.")
        
    return redirect('dashboard')

@login_required
def teacher_applications_view(request):
    try:
        teacher = Teacher.objects.get(id=request.user.id)
    except Teacher.DoesNotExist:
        messages.error(request, "Access Denied. You do not have a faculty profile.")
        return redirect('dashboard')
        
    apps = Application.objects.filter(teacher=teacher).order_by('-created_at')
    pending_apps = apps.filter(status='Pending')
    responded_apps = apps.exclude(status='Pending')
    
    return render(request, 'projects/project_applicants.html', {
        'pending_applications': pending_apps,
        'responded_applications': responded_apps,
        'teacher': teacher
    })
