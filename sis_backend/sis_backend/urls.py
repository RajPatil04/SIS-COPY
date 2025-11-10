from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os
from django.contrib.auth import views as auth_views

# API router
from rest_framework import routers
from students.api_views import StudentViewSet, AttendanceViewSet, MarkViewSet
from students.api_views import whoami, performance_analytics, student_profile_data
from students import views as student_views
from django.urls import include

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'marks', MarkViewSet, basename='mark')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/me/', whoami, name='api-whoami'),
    path('api/performance-analytics/', performance_analytics, name='api-performance-analytics'),
    path('api/student-profile/', student_profile_data, name='api-student-profile'),
    # App routes (server-rendered students index/detail/edit)
    path('students/', include('students.urls')),

    # Student and Faculty specific logins
    path('student/login/', student_views.student_login_view, name='student_login'),
    path('faculty/login/', student_views.faculty_login_view, name='faculty_login'),
    
    # Frontend HTML pages
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index'),
    # Redirect legacy frontend students.html to the server-rendered students index
    path('students.html', RedirectView.as_view(url='/students/', permanent=False), name='students'),
    path('add_student.html', TemplateView.as_view(template_name='add_student.html'), name='add_student'),
    path('attendance.html', TemplateView.as_view(template_name='attendance.html'), name='attendance'),
    path('marks.html', TemplateView.as_view(template_name='marks.html'), name='marks'),
    path('student_profile.html', TemplateView.as_view(template_name='student_profile.html'), name='student_profile'),
    path('edit_student.html', TemplateView.as_view(template_name='edit_student.html'), name='edit_student'),
    # Use Django's auth views so login posts are persisted to DB-backed users
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    # Keep legacy route for convenience
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login_page'),
]

# Serve assets (CSS, JS, images) in development
if settings.DEBUG:
    frontend_assets = os.path.join(settings.BASE_DIR, '..', 'sis_frontend_detailed - Copy', 'assets')
    urlpatterns += [
        re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': frontend_assets}),
    ]


