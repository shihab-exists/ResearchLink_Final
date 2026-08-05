from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return f"{self.code} - {self.name}"

class ResearchField(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'research_fields'

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id', primary_key=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, db_column='dept_id')
    designation = models.CharField(max_length=100)
    room_no = models.CharField(max_length=50, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    interests = models.ManyToManyField(ResearchField, db_table='teacher_interests', related_name='teachers')

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.designation})"
