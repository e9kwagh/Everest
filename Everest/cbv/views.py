
from django.forms.models import BaseModelForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
from django.contrib.auth.views import LoginView 
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView ,CreateView
from .models import Assignment ,Submission
from .forms import StudentLoginForm, AdminLoginForm ,StudentSignUpForm,AssignmentForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User





def is_admin_or_staff(user):
    return user.is_authenticated and user.is_staff



class StudentLoginView(LoginView):
    template_name = 'cbv/student_login.html'
    authentication_form = StudentLoginForm
    def get_success_url(self):
        return reverse_lazy('schedule_assignment')

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
        messages.success(self.request, "User successfully created")
        form.save()
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
        return reverse_lazy('student_login') 

    def form_valid(self, form):
        if Assignment.objects.filter(   
            delivery_time=form.cleaned_data['delivery_time'],
            deadline=form.cleaned_data['deadline']).exists():
            return self.form_invalid
        messages.success(self.request, "Assignment successfully created")
        return super().form_valid(form)
    
    def form_invalid(self, form):
     
        form.data = form.data.copy()
        form.data['delivery_time'] = '' 
        form.data['deadline'] = '' 
        messages.success(self.request, "Delivery time or deadline already in use set new one")

        return super().form_invalid(form)

 



@method_decorator(login_required(login_url=reverse_lazy('student_login')), name='dispatch')
@method_decorator(user_passes_test(is_admin_or_staff,login_url=reverse_lazy('student_login')) , name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    template_name = 'cbv/view_assignments.html'
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['math_assignments'] = context['assignments']['math']
    #     context['lesson_assignments'] = context['assignments']['lesson']
    #     del context['assignments']
    #     return context









def home(request):
    return  render(request,"cbv/base.html")