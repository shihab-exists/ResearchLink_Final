"""
URL configuration for researchlink project.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static

# Root Landing Welcome View
def root_landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

urlpatterns = [
    # Core Landing Page
    path('', root_landing_view, name='landing'),
    
    # Built-in Django Admin Interface
    path('admin/', admin.site.urls),
    
    # Custom Application Routing Modules
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('projects/', include('projects.urls')),
    path('messaging/', include('messaging.urls')),
    path('dashboard/', include('dashboard.urls')),
]

# Static & Media Asset Servicing during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
