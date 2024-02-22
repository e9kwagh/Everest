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
    path('studentview/', views.StudentView.as_view(), name='student_view'),
    path("Submitassignment/<int:assignment_id>/",views.SubmitAssignment.as_view(),name='SubmitAssignment'),
    path("updateassignment/<int:pk>/",views.UpdateAssignment.as_view(),name='UpdateAssignment'),
    path("summary",views.Summary.as_view(),name='summary'),
    path("studentprofile/<int:pk>",views.StudentDetailView.as_view(),name='student_profile'),





  
]
    # path('updateview/', views.UpdateAssignment.as_view(), name='update_view'),
    #  path('studentAssignment/', StudentAssignment.as_view(), name='studentAssignment'),