from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teacherApi import views

app_name = "teacherApi"

router = DefaultRouter()

router.register(
    "teacher", views.CRUDTeacherViewAdmin, basename="teacher_crud_operation_admin"
)

router.register(
    "teachers/public",
    views.CRUDTeacherViewPublic,
    basename="teacher_crud_operation_public",
)

router.register(
    "attendance",
    views.TeacherAttendanceRegisterView,
    basename="teacher_attendance_register",
)
router.register(
    "attendances/public",
    views.TeacherAttendanceCRUDPublicView,
    basename="teacher_attendance_register_public",
)

router.register(
    "salary",
    views.TeacherSalaryView,
    basename="teacher_salary_crud_admin",
)
router.register(
    "salarys/public",
    views.TeacherSalaryCRUDPublicView,
    basename="teacher_salary_crud_public",
)

router.register(
    "payment",
    views.TeacherSalaryPaymentStoreView,
    basename="teacher_salary_payment_public",
)

router.register(
    "homework",
    views.HomeWorkView,
    basename="home_work",
)

urlpatterns = [
    path("crud/", include(router.urls)),
    # ...............Teacher Attendance.................
    path(
        "attendance/excel/register/",
        views.TeacherAttendanceRegisterExcelView.as_view(),
        name="teacher_excel_attend_register",
    ),
    path(
        "attendance/update/",
        views.TeacherUpdateAttendanceView.as_view(),
        name="teacher_update_attendance",
    ),
    path(
        "absent/update/",
        views.TeacherAbsentUpdateView.as_view(),
        name="teacher_absent_update",
    ),
    path(
        "attendance/reset/",
        views.ResetTeacherAttendanceView.as_view(),
        name="teacher_attendance_reset",
    ),
    # ........... Teacher Slary Path ................
    path(
        "salary/excel/register/",
        views.TeacherSalaryExcelView.as_view(),
        name="teacher_excel_salary_register",
    ),
    path(
        "salary/update/",
        views.TeacherUpdateSalaryView.as_view(),
        name="teacher_update_salary",
    ),
    path(
        "salary/payment/",
        views.TeacherSalaryPaymentView.as_view(),
        name="teacher_salary_payment",
    ),
    path(
        "salary/reset/",
        views.ResetTeacherSalaryView.as_view(),
        name="teacher_salary_reset",
    ),
]
