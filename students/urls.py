from django.urls import path
from . import views

urlpatterns = [
    path('profile/edit/', views.edit_student_profile, name='student_profile_edit'),
    path('applications/', views.student_applications_view, name='student_applications'),
]
