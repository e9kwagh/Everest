from django.db import models
from django.contrib.auth.models import User



class Assignment(models.Model):
    type_field  = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200 , null = True ,blank =True)
    description  = models.TextField(max_length = 250 , null = True ,blank =True)
    delivery_time =  models.DateTimeField()
    deadline = models.DateTimeField()
    link = models.URLField(null = True)
    
    
class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_name")
    type  = models.CharField(max_length = 200)
    delivery_time =  models.DateTimeField()
    deadline = models.DateTimeField()
    Submission_link =  models.URLField(null = True)
    
    missed_deadline_count = models.IntegerField(default=0)
    on_time_submission_count = models.IntegerField(default=0)
    
