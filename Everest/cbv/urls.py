from django.contrib import admin
from django.urls import path
from  . import views
from django.contrib.auth.views import LogoutView

# from .views import StudentLoginView ,  AdminLoginView ,SignUpView

urlpatterns = [
    
    path('', views.StudentLoginView.as_view(), name='student_login'),
    path('admin-login/', views.AdminLoginView.as_view(), name='admin_login'),
    path("signup/",views.SignUpView.as_view() ,name ="signup"),
    path("home/",views.home ,name="home"),
    path('logout/', LogoutView.as_view(next_page='student_login'), name='logout'),
    path('schedule-assignment/', views.ScheduleAssignmentView.as_view(), name='schedule_assignment'),
    path('view_assignments/', views.AssignmentListView.as_view(), name='view_assignments'),

    #  path('studentAssignment/', StudentAssignment.as_view(), name='studentAssignment'),

  
]