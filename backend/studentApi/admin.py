from django.contrib import admin

from studentApi.models import (
    StudentAbsentModel,
    StudentAttendanceModel,
    StudentDataCollection,
    StudentFeeModel,
    StudentFeePaymentModel,
    StudentResultCollectionModel,
)

# Register your models here.
@admin.register(StudentDataCollection)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone", "date"]


@admin.register(StudentAttendanceModel)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "attend_day", "absent_day", "total_day"]


@admin.register(StudentAbsentModel)
class StudentAbsentAdmin(admin.ModelAdmin):
    list_display = ["student_details", "name", "date"]


@admin.register(StudentFeeModel)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "monthly_fee",
        "paid_fee",
        "unpaid_fee",
        "total_fee",
    ]


@admin.register(StudentFeePaymentModel)
class StudentFeePaymentAdmin(admin.ModelAdmin):
    list_display = ["student_details", "amount", "date"]


@admin.register(StudentResultCollectionModel)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = [
        "stu_details",
        "subject",
        "total_marks",
        "pass_marks",
        "obtained_marks",
        "gpa",
        "exam_term",
    ]
