from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_router_view, name='dashboard'),
    path('profile/edit-router/', views.edit_my_profile_view, name='my_profile'),
    path('approve-teacher/<int:teacher_id>/', views.approve_teacher_profile_view, name='approve_teacher_profile'),
]
