from django.db import models
from teachers.models import Teacher
from students.models import Student

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher_id')
    status = models.CharField(max_length=20, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.title

class Application(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, db_column='project_id')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher_id')
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'

    def __str__(self):
        return f"App by {self.student.user.username} to {self.teacher.user.username} ({self.status})"
