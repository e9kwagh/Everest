# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Assignments, Submission


class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class Math_sub_Form(forms.Form):
    math_submission_link = forms.URLField(
        label="Enter Submission Link",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control mt-2", "placeholder": "Link"}
        ),
    )


class Lesson_sub_Form(forms.Form):
    lesson_submission_link = forms.URLField(
        label="Enter Submission Link",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-1",
                "placeholder": "Enter your submission link",
            }
        ),
    )


class Math_update_Form(forms.Form):
    math_update_link = forms.URLField(
        label="Enter Submission Link",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-1",
                "placeholder": "Enter your submission link",
            }
        ),
    )


class Lesson_update_Form(forms.Form):
    lesson_update_link = forms.URLField(
        label="Enter Submission Link",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-1",
                "placeholder": "Enter your submission link",
            }
        ),
    )


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignments
        fields = [
            "title",
            "description",
            "math_send_time",
            "math_deadline",
            "lesson_send_time",
            "lesson_deadline",
            "math_question_link",
            "lesson_question_link",
        ]
        widgets = {
            "math_send_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "math_deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "lesson_send_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "lesson_deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["assigmnets", "math_sub_link", "lesson_sub_link"]


class StudentSignUpForm(UserCreationForm):
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control form-control-sm", "accept": "image/*"}
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "profile_pic",
        ]

    def check_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

    # def clean(self):
    #     cleaned_data = super().clean()
    #     self.check_username()
    #     is_superuser = self.user.is_superuser if hasattr(self, 'user') else False

    #     # Check if the user has permission to sign up
    #     if not is_superuser:
    #         self.add_error(None, forms.ValidationError('You do not have permission to sign up.'))

    #     return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get("profile_pic")

        if profile_pic:
            allowed_types = ["image/jpeg", "image/png"]
            max_size = 1 * 1024 * 1024

            if profile_pic.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Invalid file type. Please upload a valid image."
                )

            if profile_pic.size > max_size:
                raise forms.ValidationError(
                    "File size exceeds the maximum allowed size."
                )

        return profile_pic


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission

        fields = ["math_sub_link", "lesson_sub_link"]

    def clean(self):
        cleaned_data = super().clean()
        math_sub_link = cleaned_data.get("math_sub_link")
        lesson_sub_link = cleaned_data.get("lesson_sub_link")

        if not math_sub_link and not lesson_sub_link:
            raise forms.ValidationError(
                "At least one of Math Submission Link or Lesson Submission Link is required."
            )

        return cleaned_data
