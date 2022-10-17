from django.db import models

# Create your models here.


class TeacherDataCollection(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=15)
    subject = models.CharField(max_length=50)
    faculty = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    image = models.ImageField(upload_to="image/teachers/", blank=True)
    category = models.CharField(default="Academic", blank=True, max_length=50)


    def __str__(self):
        return self.name


class TeacherAttendanceModel(models.Model):
    id = models.OneToOneField(
        TeacherDataCollection, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=50)
    attend_day = models.CharField(max_length=5)
    absent_day = models.CharField(max_length=5)
    total_day = models.CharField(max_length=5)
    date = models.DateField()


class TeacherAbsentModel(models.Model):
    teacher_details = models.ForeignKey(TeacherDataCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateField()


class TeacherSalaryModel(models.Model):
    id = models.OneToOneField(
        TeacherDataCollection, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=50)
    monthly_salary = models.CharField(max_length=10)
    paid_salary = models.CharField(max_length=10)
    unpaid_salary = models.CharField(max_length=10)
    total_salary = models.CharField(max_length=10)
    date = models.DateField()


class TeacherSalaryPaymentModel(models.Model):
    teacher_details = models.ForeignKey(TeacherDataCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=20)
    date = models.DateField()


class HomeworkModel(models.Model):
    teacher_id = models.ForeignKey(TeacherDataCollection, on_delete=models.CASCADE)
    grade = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    homework = models.TextField()
    date = models.DateField()
