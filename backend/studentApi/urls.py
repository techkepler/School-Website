from django.urls import path, include
from rest_framework.routers import DefaultRouter
from studentApi import views

app_name = "studentApi"

router = DefaultRouter()

router.register(
    "student", views.CRUDStudentViewAdmin, basename="student_crud_operation_admin"
)

router.register(
    "students/public",
    views.CRUDStudentViewPublic,
    basename="student_crud_operation_public",
)

router.register(
    "attendance",
    views.StudentAttendanceRegisterView,
    basename="student_attendance_register",
)
router.register(
    "attendances/public",
    views.StudentAttendanceCRUDPublicView,
    basename="student_attendance_register_public",
)
router.register(
    "absent",
    views.StudenAbsentView,
    basename="stu_absent_view",
)

router.register(
    "fee",
    views.StudentFeeView,
    basename="student_fee_crud_admin",
)
router.register(
    "fees/public",
    views.StudentFeeCRUDPublicView,
    basename="student_fee_crud_public",
)
router.register(
    "result",
    views.StudentResultCRUDAdminView,
    basename="student_result_crud_admin",
)

urlpatterns = [
    path("crud/", include(router.urls)),
    path(
        "update/class/",
        views.StudentClassUpdateView.as_view(),
        name="student_update_class",
    ),
    path(
        "register/excel/file/",
        views.StudentRegisterExcelView.as_view(),
        name="student_register_excel",
    ),
    # ...............student Attendance.................
    path(
        "attendance/excel/register/",
        views.StudentAttendanceRegisterExcelView.as_view(),
        name="student_excel_attend_register",
    ),
    path(
        "attendance/update/",
        views.StudentUpdateAttendanceView.as_view(),
        name="student_update_attendance",
    ),
    path(
        "absent/update/",
        views.StudentAbsentUpdateView.as_view(),
        name="student_absent_update",
    ),
    path(
        "attendance/reset/",
        views.ResetStudentAttendanceView.as_view(),
        name="student_attendance_reset",
    ),
    # ........... student fee Path ................
    path(
        "fee/excel/register/",
        views.StudentFeeExcelView.as_view(),
        name="student_excel_fee_register",
    ),
    path(
        "fee/update/",
        views.StudentUpdateFeeView.as_view(),
        name="student_update_fee",
    ),
    path(
        "fee/payment/",
        views.StudentFeePaymentView.as_view(),
        name="student_fee_payment",
    ),
    path(
        "fee/reset/",
        views.ResetStudentFeeView.as_view(),
        name="student_fee_reset",
    ),
    path(
        "result/delete/",
        views.DeletStuResultView.as_view(),
        name="student_result_delete",
    ),
]
