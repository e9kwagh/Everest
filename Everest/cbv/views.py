

from django.forms.models import BaseModelForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
from django.contrib.auth.views import LoginView 
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView ,CreateView ,UpdateView
from .models import Assignment ,Submission,Student
from .forms import StudentLoginForm, AdminLoginForm ,StudentSignUpForm,AssignmentForm,Assignment_update_Form
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from .forms import Assignment_sub_Form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse





def time():
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%dT%H:%M')  
    current_now = datetime.strptime(formatted_now,'%Y-%m-%dT%H:%M')
    return current_now

def is_admin_or_staff(user):
    return user.is_authenticated and user.is_staff



class StudentLoginView(LoginView):
    template_name = 'cbv/student_login.html'
    authentication_form = StudentLoginForm
    
    def get_success_url(self):
        return reverse_lazy('student_view')

    def form_invalid(self, form):    
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

   
class AdminLoginView(LoginView):
    template_name = 'cbv/admin_login.html'
    authentication_form = AdminLoginForm
    def get_success_url(self):
        return reverse_lazy('signup')

    def form_invalid(self, form):    
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

    
class SignUpView(FormView):
    template_name = 'cbv/signup.html'
    form_class = StudentSignUpForm 
    def get_success_url(self):
        return reverse_lazy('student_login') 
    
    def form_valid(self, form) :
        username = form.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            messages.error(self.request, 'Username already exists. Please choose a different username.')
            return self.render_to_response(self.get_context_data(form=form))
        
        user= form.save()
        student = Student.objects.create(student=user)
        messages.success(self.request, "User successfully created")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong try again')      
        return self.render_to_response(self.get_context_data(form=form))




@method_decorator(login_required(login_url=reverse_lazy('student_login')), name='dispatch')
@method_decorator(user_passes_test(is_admin_or_staff), name='dispatch')
class ScheduleAssignmentView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'cbv/schedule_assignment.html'
    def get_success_url(self):
        return reverse_lazy('schedule_assignment') 

    def form_valid(self, form):
        if Assignment.objects.filter(   
            title = form.cleaned_data["title"]).exists():
            return self.form_invalid(form)
        messages.success(self.request, "Assignment successfully created")
        return super().form_valid(form)
    
    def form_invalid(self, form):
     
        form.data = form.data.copy()
        messages.error(self.request, " Title  already in use set new one")
        return super().form_invalid(form)

 



@method_decorator(login_required(login_url=reverse_lazy('student_login')), name='dispatch')
@method_decorator(user_passes_test(is_admin_or_staff,login_url=reverse_lazy('student_login')) , name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    template_name = 'cbv/admin_view.html'
    context_object_name = 'assignments'
    paginate_by = 5

    def get_queryset(self):
        assignments = Assignment.objects.all().order_by('-delivery_time')
        paginator = Paginator(assignments, self.paginate_by)
        page = self.request.GET.get('page', 1)

        try:
            page = int(page)
        except ValueError:
            page = 1

        if page < 1:
            page = 1

        if page > paginator.num_pages:
            page = paginator.num_pages

        assignments = paginator.page(page)

        return assignments




class StudentView(ListView) : 
    model = Assignment 
    template_name = 'cbv/student_view.html'
    context_object_name = 'assignments'
    paginate_by = 10
    
    def get_queryset(self) :      
        # return  Assignment.objects.filter(delivery_time__lte=formatted_now).exclude(submission__student__student=self.request.user).order_by('-created_at')
       formatted_now =time()
       return Assignment.delivery_assignment(formatted_now)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formatted_now =time()
        context["action"] =  self.request.GET.get("action")
        context["form"] =  Assignment_update_Form()   if context["action"] == "update" else Assignment_sub_Form()  
        if context["action"] == "update":
            context["assignments"] = [ {"assignment" : assignment , "ontime" : True if assignment.is_ontime() else False  } for assignment in Submission.Submited_assignment(self.request.user)  ]
        else :
                context["assignments"] =  [ { "assignment" : assignment , "is_submit" :  assignment.check_submit(self.request.user),
                                     "check_deadline" : True  if str(assignment.deadline) >= str(formatted_now) else False }  for assignment in context["assignments"] ]
        return context

def home(request):   
    return  render(request,"cbv/base.html")


class SubmitAssignment(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = Assignment_sub_Form
    template_name = 'cbv/student_view.html'
    success_url = reverse_lazy('student_view')

    def form_valid(self, form):
        assignment_id = self.kwargs['assignment_id']
        assignment = Assignment.objects.get(pk=assignment_id)
        submission_link = form.cleaned_data['submission_link']
        student, created = Student.objects.get_or_create(student=self.request.user)     
        current_now = time()
        
        submission = form.save(commit=False)
        submission.student = student
        submission.assignment = assignment
        submission.submission_link = submission_link
        submission.submission_time = current_now
        submission.save()

       
        return super().form_valid(form)
    
    def form_invalid(self, form) :
        messages.error(self.request, "Try again something went wrong")
        return super().form_invalid(form)

class UpdateAssignment(UpdateView) :
    model = Submission 
    form_class =  Assignment_update_Form
    template_name = 'cbv/student_view.html'
      
    def get_success_url(self):
         return reverse('student_view') + f'?action=update'
   
    def form_invalid(self,form) :
        id  = self.kwargs["assignment_id"]
        submission = Submission.objects.get(pk=id)
        link = form.cleaned_data["submission_link"]
        submission.submission_link = link
        return super().form_invalid(form)
    
    




  # submission = Submission.objects.create(
        #     student=student,
        #     assignment = assignment , 
        #     submission_link=submission_link,
        #     submission_time = current_now,  
        # )
        # need to user try and except