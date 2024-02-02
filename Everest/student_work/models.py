from django.db import models
from django.contrib.auth.models import User


class Assignments(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_assignments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=150, blank=True)
    is_submitted = models.BooleanField(default=False)

    math_send_time = models.DateTimeField()
    math_deadline = models.DateTimeField()
    math_question_link = models.URLField()

    lesson_send_time = models.DateTimeField()
    lesson_deadline = models.DateTimeField()
    lesson_question_link = models.URLField()

    def __str__(self):
        return str(self.title)


class Submission(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="student_name"
    )
    assigmnets = models.ForeignKey(Assignments, on_delete=models.CASCADE)

    math_sub_link = models.URLField(null=True, blank=True)
    math_sub_date = models.DateTimeField(null=True, blank=True)

    lesson_sub_link = models.URLField(null=True, blank=True)
    lesson_sub_date = models.DateTimeField(null=True, blank=True)

    missed_deadline_count = models.IntegerField(default=0)
    on_time_submission_count = models.IntegerField(default=0)
