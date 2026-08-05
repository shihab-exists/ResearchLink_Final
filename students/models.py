from django.db import models
from django.contrib.auth.models import User
from teachers.models import Department

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'skills'

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id', primary_key=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, db_column='dept_id')
    roll_no = models.CharField(max_length=20, unique=True)
    cgpa = models.DecimalField(decimal_places=2, max_digits=3)
    bio = models.TextField(blank=True, null=True)
    cv_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField(Skill, db_table='student_skills', related_name='students')

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.roll_no})"
