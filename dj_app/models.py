# Create your models here.
from django.db import models


class StudentAddress(models.Model):
    stu_pin_code = models.CharField(primary_key=True, max_length=6)
    stu_state = models.CharField(max_length=20, blank=True, null=True)
    student_city = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'student_address'


class StudentBranchDetails(models.Model):
    stu_branch = models.CharField(primary_key=True, max_length=20)
    subjects = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'student_branch_details'


class StudentDetails(models.Model):
    stu_id = models.CharField(primary_key=True, max_length=8)
    stu_name = models.CharField(max_length=20, blank=True, null=True)
    stu_branch = models.ForeignKey(StudentBranchDetails, on_delete = models.CASCADE, db_column='stu_branch', blank=True, null=True)
    stu_pin_code = models.ForeignKey(StudentAddress, on_delete = models.CASCADE, db_column='stu_pin_code', blank=True, null=True)

    class Meta:
        db_table = 'student_details'
