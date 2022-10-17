from django.urls import path, include
from rest_framework.routers import DefaultRouter
from staffApi import views

app_name = "staffApi"

router = DefaultRouter()

router.register(
    "staff", views.CRUDStaffViewAdmin, basename="staff_crud_operation_admin"
)

router.register(
    "staffs/public",
    views.CRUDStaffViewPublic,
    basename="staff_crud_operation_public",
)

router.register(
    "attendance",
    views.StaffAttendanceRegisterView,
    basename="staff_attendance_register",
)
router.register(
    "attendances/public",
    views.StaffAttendanceCRUDPublicView,
    basename="staff_attendance_register_public",
)

router.register(
    "salary",
    views.StaffSalaryView,
    basename="staff_salary_crud_admin",
)
router.register(
    "salarys/public",
    views.StaffSalaryCRUDPublicView,
    basename="staff_salary_crud_public",
)

urlpatterns = [
    path("crud/", include(router.urls)),
    # ...............staff Attendance.................
    path(
        "attendance/excel/register/",
        views.StaffAttendanceRegisterExcelView.as_view(),
        name="staff_excel_attend_register",
    ),
    path(
        "attendance/update/",
        views.StaffUpdateAttendanceView.as_view(),
        name="staff_update_attendance",
    ),
    path(
        "absent/update/",
        views.StaffAbsentUpdateView.as_view(),
        name="staff_absent_update",
    ),
    path(
        "attendance/reset/",
        views.ResetStaffAttendanceView.as_view(),
        name="staff_attendance_reset",
    ),
    # ........... staff Slary Path ................
    path(
        "salary/excel/register/",
        views.StaffSalaryExcelView.as_view(),
        name="staff_excel_salary_register",
    ),
    path(
        "salary/update/",
        views.StaffUpdateSalaryView.as_view(),
        name="staff_update_salary",
    ),
    path(
        "salary/payment/",
        views.StaffSalaryPaymentView.as_view(),
        name="staff_salary_payment",
    ),
    path(
        "salary/reset/",
        views.ResetStaffSalaryView.as_view(),
        name="staff_salary_reset",
    ),
]
