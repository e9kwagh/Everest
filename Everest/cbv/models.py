"""models.py"""

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def assignment(self):
        """assignment"""
        
        result = []

        assignments = Assignment.objects.all()
        for assignment in assignments:
            data = {}
            on_time = False
            deadline = True
            is_submited = assignment.is_submited(self)
            if is_submited:
                on_time = assignment.submission.get(student=self).is_ontime()
                deadline = False if on_time else False

            data = {
                "assignment": assignment.title,
                "on_time": on_time,
                "is_submited": is_submited,
                "deadline": deadline,
            }

            result.append(data)
        return result

    def summary(self):
        """summary"""
        students = Student.objects.filter(student__is_staff=False)
        summary_record = []

        for student in students:
            data = {}
            submissions = student.submission.filter(student=self)
            print("submissions now =  : ", submissions)
            total = submissions.count()
            deadline, ontime = 0, 0
            for submission in submissions:
                if submission.is_ontime():
                    ontime += 1
                else:
                    deadline += 1

            data = {
                "username": student.student.username,
                "ontime": ontime,
                "deadline": deadline,
                "total": total,
            }
            summary_record.append(data)
        return summary_record


class Assignment(models.Model):
    """Assignment"""

    category = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    assignment_link = models.TextField(unique=False) # change it to the textfield
    delivery_time = models.DateTimeField()
    deadline = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

       


    def check_submit(self,user) :
        return self.submission.filter(student__student= user).exists()
    

    @classmethod
    def delivery_assignment(cls,time):
        return cls.objects.filter(delivery_time__lte = time).order_by("-delivery_time")
    
    # new way, updated of 6/02/24

    def is_submited(self, user):
        try:
            submission = self.submission.get(student=user)
            return True
        except:
            return False

    def users(self):
        """users"""
        result = []

        students = Student.objects.all()
        for student in students:
            data = {}
            on_time = False
            deadline = False
            is_submited = self.is_submited(student)
            if is_submited:
                on_time = self.submission.get(student=student).is_ontime()
                deadline = False if on_time else True
            data = {
                "student": student.student.username,
                "on_time": on_time,
                "is_submited": is_submited,
                "deadline": deadline,
            }

            result.append(data)
        return result

    def check_status(self, user):
        """check_status"""
        try:
            submission = self.submission.get(student=user)
            if submission.submission_time >= self.deadline:
                return "deleyed"
            return "ontime"

        except:
            return "not exits"

    @classmethod
    def check_all_user(cls):
        """check_all_user"""
        users = User.objects.filter(is_staff=False)
        submission_record = {user.username: cls.check_status(user) for user in users}
        return submission_record

    # to get all the submited assignments for that  user  , one user many assignments
    @classmethod
    def all_submission(cls, user):
        """all_submission"""
        return cls.objects.filter(submission__student=user)

    @classmethod
    def submission_status(cls, student):
        submissions = cls.all_submission(student)
        total = submissions.count()
        deadline_count, ontime_count = 0, 0
        for submission in submissions:
            if submission.submission_time > submission.assignment.deadline:
                deadline_count += 1
            else:
                ontime_count += 1

        return {
            "total": total,
            "deadline_count": deadline_count,
            "ontime_count": ontime_count,
        }

    @classmethod
    def status_of_user(cls):
        student_record = {}
        students = Student.objects.filter(student__is_staff=False)
        # users = User.objects.filter()
        for student in students:
            student_record[student.student.username] = cls.submission_status(student)
        return student_record


class Submission(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="submission"
    )
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submission"
    )

    submission_link = models.TextField(unique=False)
    submission_time = models.DateTimeField(null =True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("assignment", "student")

    def is_ontime(self):
        return self.assignment.deadline >= self.submission_time
    
    @classmethod
    def Submited_assignment(cls,user):
        return cls.objects.filter(student__student = user).order_by("-submission_time")

    
    

    # black models.py
    # reformatted models.py

    # All done! ✨ 🍰 ✨
    # 1 file reformatted.
