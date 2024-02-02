from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("signuppage", views.signupPage, name="signuppage"),
    path("", views.student_login, name="studentlogin"),
    path("adminlogin", views.admin_login, name="adminlogin"),
    path("dashsboard", views.dashboard, name="dashboard"),
    path("logout/", views.logout_fun, name="logout"),
    path("schedule_assignment", views.schedule_assignment, name="schedule_assignment"),
    path("all_assignments", views.all_assignments, name="all_assignments"),
    path(
        "mathassignment/<int:assignment_id>/",
        views.submit_math_assignment,
        name="submit_math_assignment",
    ),
    path(
        "lessonassignment/<int:assignment_id>/",
        views.submit_lesson_assignment,
        name="submit_lesson_assignment",
    ),
    path("admintracker", views.admin_tracker, name="admin_tracker"),
    path("student_tracker", views.student_tracker, name="student_tracker"),
    path("update_math/<int:assignment_id>/", views.update_math, name="update_math"),
    path(
        "update_lesson/<int:assignment_id>/", views.update_lesson, name="update_lesson"
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
