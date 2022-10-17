from pyexpat import model
from django.contrib import admin

from infoApi.models import (
    AdmissionInquiryModel,
    AnnouncementModel,
    BlogModel,
    CalendarEventModel,
    EventsModel,
    GalleryModel,
    LeaveApplicationModel,
    NewsModel,
    RoutineModel,
)

# Register your models here.


@admin.register(AnnouncementModel)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "date"]


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "date"]


@admin.register(BlogModel)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "date"]


@admin.register(EventsModel)
class EventsAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "date"]


@admin.register(CalendarEventModel)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ["event_id", "subject", "location"]


@admin.register(RoutineModel)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ["subject", "grade", "date", "exam_term"]


@admin.register(LeaveApplicationModel)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ["name", "grade", "status", "date"]


@admin.register(AdmissionInquiryModel)
class AdmissionInquiryAdmin(admin.ModelAdmin):
    list_display = ["guardian_name", "email", "phone_number", "year_applying"]


@admin.register(GalleryModel)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["name", "date"]
