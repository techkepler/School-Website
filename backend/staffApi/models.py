from django.db import models

# Create your models here.


class StaffDataCollection(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=15)
    position = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    image = models.ImageField(upload_to="image/Staffs/", blank=True)
    category = models.CharField(default="Administrative", blank=True, max_length=50)

    def __str__(self):
        return self.name


class StaffAttendanceModel(models.Model):
    id = models.OneToOneField(
        StaffDataCollection, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=50)
    attend_day = models.CharField(max_length=5)
    absent_day = models.CharField(max_length=5)
    total_day = models.CharField(max_length=5)
    date = models.DateField()


class StaffAbsentModel(models.Model):
    staff_details = models.ForeignKey(StaffDataCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateField()


class StaffSalaryModel(models.Model):
    id = models.OneToOneField(
        StaffDataCollection, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=50)
    monthly_salary = models.CharField(max_length=10)
    paid_salary = models.CharField(max_length=10)
    unpaid_salary = models.CharField(max_length=10)
    total_salary = models.CharField(max_length=10)
    date = models.DateField()


class StaffSalaryPaymentModel(models.Model):
    staff_details = models.ForeignKey(StaffDataCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=20)
    date = models.DateField()
