from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_projects_view, name='manage_projects'),
    path('create/', views.create_project_view, name='create_project'),
    path('edit/<int:project_id>/', views.edit_project_view, name='edit_project'),
    path('delete/<int:project_id>/', views.delete_project_view, name='delete_project'),
    path('apply/<int:teacher_id>/', views.apply_supervision_view, name='apply_supervision'),
    path('respond/<int:application_id>/<str:status>/', views.respond_application_view, name='respond_application'),
    path('applications/', views.teacher_applications_view, name='teacher_applications'),
]
