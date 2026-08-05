from django.urls import path
from . import views

urlpatterns = [
    path('profile/edit/', views.edit_teacher_profile, name='teacher_profile_edit'),
    path('browse/', views.browse_teachers, name='browse_teachers'),
    path('view/<int:teacher_id>/', views.view_teacher_profile, name='view_teacher_profile'),
]
