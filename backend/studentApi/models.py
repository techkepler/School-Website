from django.db import models

# Create your models here.
class StudentDataCollection(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=15)
    grade = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.name


# Student Attendance Models


class StudentAttendanceModel(models.Model):
    id = models.OneToOneField(
        StudentDataCollection, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=20, default="One")
    attend_day = models.CharField(max_length=5)
    absent_day = models.CharField(max_length=5)
    total_day = models.CharField(max_length=5)
    date = models.DateField()


class StudentAbsentModel(models.Model):
    student_details = models.ForeignKey(StudentDataCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateField()


# Student Fee Models


class StudentFeeModel(models.Model):
    id = models.OneToOneField(
        StudentDataCollection, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=20, default="One")
    monthly_fee = models.IntegerField()
    bus_fee = models.IntegerField()
    computer_fee = models.IntegerField()
    paid_fee = models.BigIntegerField()
    unpaid_fee = models.BigIntegerField()
    total_fee = models.BigIntegerField()
    date = models.DateField()


class StudentFeePaymentModel(models.Model):
    student_details = models.ForeignKey(StudentDataCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    date = models.DateField()


# Student Result Model


class StudentResultCollectionModel(models.Model):
    stu_details = models.ForeignKey(StudentDataCollection, on_delete=models.CASCADE)
    grade = models.CharField(max_length=50, default="One")
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    total_marks = models.IntegerField()
    pass_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    gpa = models.CharField(max_length=5)
    exam_term = models.CharField(max_length=15)
