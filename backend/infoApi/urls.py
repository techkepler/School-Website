from django.urls import path, include
from rest_framework.routers import DefaultRouter
from infoApi import views

app_name = "infoApi"

router = DefaultRouter()

router.register(
    "announcement",
    views.AnnoucementAdminView,
    basename="announcement_crud_operation_admin",
)

router.register(
    "public/announcement",
    views.AnnoucementPublicView,
    basename="announcements_public",
)

router.register(
    "news",
    views.NewsAdminView,
    basename="news_crud_operation_admin",
)
router.register(
    "public/news",
    views.NewsPublicView,
    basename="news_public",
)

router.register(
    "blogs",
    views.BlogsAdminView,
    basename="blogs_crud_operation_admin",
)

router.register(
    "public/blogs",
    views.BlogsPublicView,
    basename="blogs_public",
)

router.register(
    "events",
    views.EventsAdminView,
    basename="events_crud_operation_admin",
)
router.register(
    "public/events",
    views.EventsPublicView,
    basename="events_public",
)

router.register(
    "calendar",
    views.CalendarEventView,
    basename="calendar_crud_operation_admin",
)

router.register(
    "routines",
    views.RoutineAdminView,
    basename="routine_crud_operation_admin",
)

router.register(
    "leave/application",
    views.LeaveApplicationView,
    basename="application_crud_operation_admin",
)

router.register(
    "admission/inquiry",
    views.AdmissionInquiryView,
    basename="admission_inquiry_crud_operation_admin",
)

router.register(
    "gallery",
    views.GalleryView,
    basename="gallery_crud_operation_admin",
)

urlpatterns = [
    path("crud/", include(router.urls)),
    path(
        "routine/excel/file/",
        views.RoutineExcelView.as_view(),
        name="routine_excel_view",
    ),
    path(
        "calendar/add/event/",
        views.CalendarEventApiView.as_view(),
        name="calendar_event_add",
    ),
]
