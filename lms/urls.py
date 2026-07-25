"""
URL configuration for lms project.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Required for Media Files
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return redirect("login")


urlpatterns = [

    # Home
    path("", home, name="home"),

    # Admin
    path("admin/", admin.site.urls),

    # Authentication
    path("", include("accounts.urls")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # Institution
    path("institution/", include("institution.urls")),
    path("department/", include("department.urls")),
    path("course/", include("course.urls")),
    path("students/", include("student.urls")),
    path("staff/", include("staff.urls")),
    path("subject/", include("subject.urls")),
    path("staff-panel/", include("staff_panel.urls")),
    
    ]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )