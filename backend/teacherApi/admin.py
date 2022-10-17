from django.contrib import admin
from .models import (
    HomeworkModel,
    TeacherAbsentModel,
    TeacherAttendanceModel,
    TeacherDataCollection,
    TeacherSalaryModel,
    TeacherSalaryPaymentModel,
)

# Register your models here.


@admin.register(TeacherDataCollection)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone"]


@admin.register(TeacherAttendanceModel)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "attend_day", "absent_day", "total_day"]


@admin.register(TeacherAbsentModel)
class TeacherAbsentAdmin(admin.ModelAdmin):
    list_display = ["teacher_details", "name", "date"]


@admin.register(TeacherSalaryModel)
class TeacherSalaryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "monthly_salary",
        "paid_salary",
        "unpaid_salary",
        "total_salary",
    ]


@admin.register(TeacherSalaryPaymentModel)
class TeacherSalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ["teacher_details", "amount", "date"]


@admin.register(HomeworkModel)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ["teacher_id", "grade", "subject", "date"]
