from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.index, name='students_index'),
    path('login/', views.student_login_view, name='student_login'),
    path('profile/', views.student_profile_view, name='student_profile'),
    path('faculty-login/', views.faculty_login_view, name='faculty_login'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/edit/', views.student_edit, name='student_edit'),
]
