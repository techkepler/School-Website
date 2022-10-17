from django.contrib import admin
from .models import (
    StaffAbsentModel,
    StaffAttendanceModel,
    StaffDataCollection,
    StaffSalaryModel,
    StaffSalaryPaymentModel,
)

# Register your models here.


@admin.register(StaffDataCollection)
class StaffAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone"]


@admin.register(StaffAttendanceModel)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "attend_day", "absent_day", "total_day"]

@admin.register(StaffAbsentModel)
class StaffAbsentAdmin(admin.ModelAdmin):
    list_display = ["staff_details", "name", "date"]


@admin.register(StaffSalaryModel)
class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "monthly_salary",
        "paid_salary",
        "unpaid_salary",
        "total_salary",
    ]


@admin.register(StaffSalaryPaymentModel)
class StaffSalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ["staff_details", "amount", "date"]
