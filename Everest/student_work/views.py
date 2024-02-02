from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import (
    StudentLoginForm,
    AdminLoginForm,
    Math_update_Form,
    Lesson_update_Form,
    Math_sub_Form,
    Lesson_sub_Form,
    StudentSignUpForm,
    AssignmentForm,
)
from .models import Assignments, Submission
from django.db.models import Q
from django.utils import timezone

from django.db import connection

import pytz
from datetime import timedelta
from django.db.models import Sum


def dashboard(request):
    return render(request, "student_work/dashboard.html")


def current_time():
    current_time_local = timezone.localtime(timezone.now())
    now = current_time_local.strftime("%Y-%m-%dT%H:%M")
    print(now)


def time_stamp():
    timezone.activate("Asia/Kolkata")
    current_time = timezone.localtime(timezone.now())
    formatted_current = current_time.strftime("%Y-%m-%dT%H:%M")
    formatted_current_time = timezone.datetime.strptime(
        formatted_current, "%Y-%m-%dT%H:%M"
    )
    now = formatted_current_time
    return now


def all_assignments(request):
    now = time_stamp()
    now_utc = now.astimezone(pytz.utc)

    math_assignments = Assignments.objects.filter(math_send_time__lt=now_utc).order_by(
        "-math_send_time"
    )
    lesson_assignments = Assignments.objects.filter(
        lesson_send_time__lt=now_utc
    ).order_by("-lesson_send_time")

    math_data = [
        {
            "math_id": assignment.id,
            "title": assignment.title,
            "link": assignment.math_question_link,
            "deadline": timezone.localtime(assignment.math_deadline),
            "send_time": timezone.localtime(assignment.math_send_time),
            "assignment_type": "math",
        }
        for assignment in math_assignments
    ]

    lesson_data = [
        {
            "lesson_id": assignment.id,
            "title": assignment.title,
            "link": assignment.lesson_question_link,
            "deadline": timezone.localtime(assignment.lesson_deadline),
            "send_time": timezone.localtime(assignment.lesson_send_time),
            "assignment_type": "lesson",
        }
        for assignment in lesson_assignments
    ]

    math_sub_Form = Math_sub_Form()
    lesson_sub_Form = Lesson_sub_Form()

    items_per_page = 5

    # Page math
    math_page = request.GET.get("math_page", 1)
    math_paginator = Paginator(math_data, items_per_page)

    if not str(math_page).isdigit():
        math_page = 1
    else:
        math_page = int(math_page)

    if math_page < 1:
        math_page = 1
    elif math_page > math_paginator.num_pages:
        math_page = math_paginator.num_pages

    math_data_page = math_paginator.page(math_page)

    # lesson_page
    lesson_page = request.GET.get("lesson_page", 1)
    lesson_paginator = Paginator(lesson_data, items_per_page)

    if not str(lesson_page).isdigit():
        lesson_page = 1
    else:
        lesson_page = int(lesson_page)

    if lesson_page < 1:
        lesson_page = 1
    elif lesson_page > lesson_paginator.num_pages:
        lesson_page = lesson_paginator.num_pages

    lesson_data_page = lesson_paginator.page(lesson_page)

    context = {
        "current_time": now,
        "math_data": math_data_page,
        "lesson_data": lesson_data_page,
        "math_sub_Form": math_sub_Form,
        "lesson_sub_Form": lesson_sub_Form,
    }

    return render(request, "student_work/all_assignments.html", context)


@login_required(login_url="studentlogin")
def submit_math_assignment(request, assignment_id):
    if request.method == "POST":
        assignment = get_object_or_404(Assignments, id=assignment_id)
        form = Math_sub_Form(request.POST)
        # current_time = timezone.now()
        # current_time = current_time.astimezone(timezone.get_current_timezone())

        # current_time_local = timezone.localtime(timezone.now())
        # now = current_time_local.strftime('%Y-%m-%dT%H:%M')
        # print(now)

        # right_format = assignment.math_deadline
        # format_used = right_format.strftime("%Y-%m-%dT%H:%M:%S%z")
        # formatted_current_time = current_time.strftime(format_used)
        now = time_stamp()
        now_utc = now.astimezone(pytz.utc)

        if form.is_valid():
            submission_link = form.cleaned_data["math_submission_link"]

            submission, created = Submission.objects.get_or_create(
                assigmnets=assignment, student=request.user
            )

            submission.math_sub_link = submission_link
            submission.math_sub_date = now_utc

            if submission.math_sub_date <= assignment.math_deadline:
                submission.on_time_submission_count += 1
            else:
                submission.missed_deadline_count += 1

            submission.save()
            messages.success(request, "Math Assignment submitted successfully.")
            return redirect("all_assignments")
        else:
            messages.error(request, "somthing went wrong")
            return redirect("all_assignments")
    return render(request, "student_work/all_assignments.html")


@login_required(login_url="studentlogin")
def submit_lesson_assignment(request, assignment_id):
    if request.method == "POST":
        assignment = get_object_or_404(Assignments, id=assignment_id)
        form = Lesson_sub_Form(request.POST)
        now = time_stamp()
        now_utc = now.astimezone(pytz.utc)

        if form.is_valid():
            submission_link = form.cleaned_data["lesson_submission_link"]

            submission, created = Submission.objects.get_or_create(
                student=request.user, assigmnets=assignment
            )
            submission.lesson_sub_link = submission_link
            submission.lesson_sub_date = now_utc

            if submission.lesson_sub_date <= assignment.lesson_deadline:
                submission.on_time_submission_count += 1
            else:
                submission.missed_deadline_count += 1

                print("assignment.lesson_deadline", assignment.lesson_deadline)

            submission.save()
            messages.success(request, "Math Assignment submitted successfully.")
            return redirect("all_assignments")
        else:
            messages.error(request, "somthing went wrong")
            return redirect("all_assignments")
    return render(request, "student_work/all_assignments.html")


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser, login_url="adminlogin")
def admin_tracker(request):
    Student_tracking_data = (
        Submission.objects.values("student__username")
        .annotate(
            missed_deadline_count=Sum("missed_deadline_count"),
            on_time_submission_count=Sum("on_time_submission_count"),
        )
        .order_by("student__username")
    )

    # student_first_name = Student_tracking_data.student.first_name
    # print(student_first_name)

    # print("all of Student_tracking_data" ,Student_tracking_data )
    context = {"datas": Student_tracking_data}
    return render(request, "student_work/admintracker.html", context)


@login_required(login_url="studentlogin")
def student_tracker(request):
    math_submissions = Submission.objects.filter(
        student=request.user, math_sub_link__isnull=False, math_sub_date__isnull=False
    ).order_by("-math_sub_date")

    print("math_submissions", math_submissions)

    lesson_submissions = Submission.objects.filter(
        student=request.user,
        lesson_sub_link__isnull=False,
        lesson_sub_date__isnull=False,
    ).order_by("-lesson_sub_date")

    math_update_Form = Math_update_Form()
    lesson_update_Form = Lesson_update_Form()

    context = {
        "math_submissions": math_submissions,
        "lesson_submissions": lesson_submissions,
        "math_update_Form": math_update_Form,
        "lesson_update_Form": lesson_update_Form,
    }

    return render(request, "student_work/student_tracker.html", context)


def update_math(request, assignment_id):
    print("assignment_id", assignment_id)
    if request.method == "POST":
        submission = Submission.objects.get(pk=assignment_id)
        form = Math_update_Form(request.POST)
        print("submission : ", submission)
        if form.is_valid():
            link = form.cleaned_data["math_update_link"]
            submission.math_sub_link = link
            submission.save()
            messages.success(request, f" successfully updated the assignmnet")
            return redirect("student_tracker")
        else:
            messages.error(request, "something went wrong try again")

            return redirect("student_tracker")


def update_lesson(request, assignment_id):
    if request.method == "POST":
        submission = Submission.objects.get(pk=assignment_id, student=request.user)
        form = Lesson_update_Form(request.POST)
        if form.is_valid():
            link = form.cleaned_data["lesson_update_link"]
            submission.lesson_sub_link = link
            submission.save()
            messages.success(request, f" successfully updated the assignmnet")
            return redirect("student_tracker")
        else:
            messages.error(request, "something went wrong try again")
    return redirect("student_tracker")


@user_passes_test(is_superuser)
def schedule_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        print("post")
        if form.is_valid():
            scheduled_date = form.cleaned_data["math_send_time"].date()
            # ist = pytz.timezone('Asia/Kolkata')
            # math_send_time = form.cleaned_data["math_send_time"].replace(tzinfo=timezone.utc).astimezone(ist)
            # math_deadline = form.cleaned_data["math_deadline"].replace(tzinfo=timezone.utc).astimezone(ist)

            # lesson_send_time = form.cleaned_data["lesson_send_time"].replace(tzinfo=timezone.utc).astimezone(ist)
            # lesson_deadline = form.cleaned_data["lesson_deadline"].replace(tzinfo=timezone.utc).astimezone(ist)

            # existing_assignment = Assignments.objects.filter(math_send_time__date=scheduled_date).first()

            # if existing_assignment:

            #     return render(request, 'student_work/firm_update_as.html', {'existing_assignment': existing_assignment, 'new_assignment': form})
            # else:
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, "Assignment scheduled successfully.")

            return redirect("schedule_assignment")
    else:
        form = AssignmentForm()
    return render(request, "student_work/schedule_assignment.html", {"form": form})


def student_login(request):
    if request.method == "POST":
        form = StudentLoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect("all_assignments")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = StudentLoginForm(request)

    return render(request, "student_work/s_loginpage.html", {"form": form})


def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user and user.is_superuser:
                login(request, user)
                messages.success(request, "Logged in successfully as superuser.")
                return redirect("schedule_assignment")
            else:
                messages.error(request, "Invalid username or password for superuser.")
                return redirect("adminlogin")
    else:
        form = AdminLoginForm(request)

    return render(request, "student_work/adminlogin.html", {"form": form})


@login_required
def logout_fun(request):
    logout(request)
    messages.success(request, "succesfully logout ")
    return redirect("studentlogin")


@user_passes_test(is_superuser, login_url="adminlogin")
def signupPage(request):
    if request.method == "POST":
        if not request.user.is_superuser:
            messages.error(request, "You do not have permission to sign up.")
            return redirect("home")

        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print("in_valid")
            user = form.save()
            messages.success(request, "Acount created succesfully ")
            return redirect("signupPage")
        else:
            messages.error(request, "try again with another user name and password ")
            print(form.errors)
            return redirect("signuppage")

        # else:
        #   for field, errors in form.errors.items():
        #         for error in errors:
        #             messages.error(request, f'{field}: {error}')
        #   return render(request,"student_work/signuppage.html",context)

    else:
        form = StudentSignUpForm()
    context = {"form": form}
    return render(request, "student_work/signuppage.html", context)


# @login_required
# def submit_assignment(request, assignment_id, assignment_type):

#     current_time = timezone.now()
#     current_time = current_time.astimezone(timezone.get_current_timezone())

#     right_format = Assignments.objects.values("math_send_time").first()
#     format_used = right_format['math_send_time'].strftime('%Y-%m-%dT%H:%M:%S%z')
#     formatted_current_time = current_time.strftime(format_used)


#     assignment = Assignments.objects.get(pk=assignment_id)
#     submission, created = Submission.objects.get_or_create(student=request.user, assignment=assignment)

#     if request.method == 'POST':
#         form = AssignmentSubmissionForm(request.POST)
#         if form.is_valid():
#             if assignment_type == 'math':
#                 submission.math_sub_link = form.cleaned_data['math_answer_link']
#                 submission.math_sub_link = timezone.now()
#             elif assignment_type == 'lesson':
#                 submission.lesson_sub_link = form.cleaned_data['lesson_answer_link']
#                 submission.lesson_sub_link = timezone.now()


#             if formatted_current_time <= assignment.math_deadline and submission.math_sub_link:
#                 submission.on_time_submission_count += 1

#             if formatted_current_time <= assignment.lesson_deadline and submission.lesson_sub_link:
#                 submission.on_time_submission_count += 1

#             if formatted_current_time > assignment.math_deadline and not submission.math_sub_link:
#                 submission.missed_deadline_count += 1

#             if formatted_current_time > assignment.lesson_deadline and not submission.lesson_sub_link:
#                 submission.missed_deadline_count += 1

#             submission.save()
#             messages.success(request, 'Assignment submitted successfully.')
#             return redirect('student_dashboard')
#     else:
#         form = AssignmentSubmissionForm()

#     return render(request, 'submit_assignment.html', {'form': form, 'assignment': assignment, 'assignment_type': assignment_type})


# @login_required
# def submit_lesson_assignment(request, assignment_id):
#     assignment = Assignments.objects.get(pk=assignment_id)

#     if request.method == 'POST':
#         form = Lesson_sub_Form(request.POST)
#         if form.is_valid():
#             submission_link = form.cleaned_data['lesson_submission_link']


#             submission, created = Submission.objects.get_or_create(student=request.user, assignment=assignment)
#             submission.lesson_sub_link = submission_link
#             submission.lesson_sub_date = timezone.now()
#             submission.save()

#             messages.success(request, 'Lesson Assignment submitted successfully.')
#             return redirect('student_dashboard')

#     return render(request, 'student_work/all_assignments.html')

# @user_passes_test(is_superuser)
# def see_all_assig(request) :
#     math_assig =  Assignments.objects.filter() ).all()
