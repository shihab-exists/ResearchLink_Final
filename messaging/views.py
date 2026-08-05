from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message
from teachers.models import Teacher
from students.models import Student

@login_required
def chat_list_view(request, contact_id=None):
    # Fetch all messages sent or received by current user
    msg_history = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-sent_at')
    
    # Determine potential message recipients
    user_role = request.session.get('user_role')
    recipients = []
    
    if user_role == 'student':
        # Students can send messages to approved teachers
        approved_teachers = Teacher.objects.filter(is_approved=True)
        recipients = User.objects.filter(id__in=approved_teachers.values_list('id', flat=True))
    elif user_role == 'teacher':
        # Teachers can send messages to all students
        all_students = Student.objects.all()
        recipients = User.objects.filter(id__in=all_students.values_list('id', flat=True))
    
    # Handle Send Message from form
    if request.method == 'POST':
        rec_id = request.POST.get('receiver')
        text = request.POST.get('message_text')
        
        if rec_id and text:
            receiver_user = get_object_or_404(User, id=int(rec_id))
            Message.objects.create(
                sender=request.user,
                receiver=receiver_user,
                message_text=text
            )
            messages.success(request, f"Your message was successfully sent to {receiver_user.first_name} {receiver_user.last_name}!")
            return redirect('chat_list')
            
    # Optional shortcut for opening from direct "Message Supervisor" buttons
    preselected_receiver = None
    if contact_id:
        preselected_receiver = get_object_or_404(User, id=contact_id)
        
    return render(request, 'messaging/chat_list.html', {
        'msg_history': msg_history,
        'recipients': recipients,
        'preselected_receiver': preselected_receiver
    })

@login_required
def send_message_view(request, receiver_id):
    # Backward compatibility handler for quick links
    if request.method == 'POST':
        text = request.POST.get('message_text')
        receiver = get_object_or_404(User, id=receiver_id)
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                message_text=text
            )
            messages.success(request, f"Your message has been sent to {receiver.first_name}!")
            
    return redirect('chat_list')
