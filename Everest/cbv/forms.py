from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from .models import Assignment ,Submission

class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class Assignment_sub_Form(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_link']
        labels = {'submission_link': 'Enter Submission Link'}
        widgets = {
            'submission_link': forms.TextInput(
                attrs={
                    'class': 'form-control mt-2',
                    'placeholder': 'Enter your submission link',
                }
            ),
        }

class Assignment_update_Form(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_link']
        labels = {'submission_link': 'Enter Updated Link'}
        widgets = {
            'submission_link': forms.TextInput(
                attrs={
                    'class': 'form-control mt-2',
                    'placeholder': 'Enter your updated link',
                }
            ),
        }
        
class StudentSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            
        ]




class AssignmentForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('Lesson','lesson' ),
        ('Math','math' ),
        ('Other','other'),
    ]

    category = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # other_text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows': 3}))
    assignment_link = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Assignment
        fields = [
            'category',
            'title',
            'description',
            'delivery_time',
            'deadline',
            'assignment_link'
        ]
        widgets = {
            'delivery_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
        }
