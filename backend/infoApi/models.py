from django.db import models
from studentApi.models import StudentDataCollection
# Create your models here.


class AnnouncementModel(models.Model):
    title = models.CharField(max_length=300)
    data = models.TextField()
    status = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)


class TinyMceAnnouncementModel(models.Model):
    data = models.TextField()


class NewsModel(models.Model):
    title = models.CharField(max_length=300)
    data = models.TextField()
    short_details = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to="image/news", blank=True)
    date = models.DateField(auto_now_add=True)


class BlogModel(models.Model):
    title = models.CharField(max_length=300)
    data = models.TextField()
    short_details = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    author_name = models.CharField(max_length=100)
    author_img = models.ImageField(upload_to="image/author", blank=True)
    image = models.ImageField(upload_to="image/news", blank=True)
    date = models.DateField(auto_now_add=True)


class EventsModel(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    status = models.BooleanField(default=True)


class CalendarEventModel(models.Model):
    event_id = models.CharField(max_length=1000, primary_key=True)
    subject = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    all_day = models.BooleanField(default=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)


class RoutineModel(models.Model):
    grade = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    exam_term = models.CharField(max_length=50)


class LeaveApplicationModel(models.Model):
    stu_id = models.ForeignKey(StudentDataCollection, on_delete=models.CASCADE)
    grade = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=50, default="pending")


class AdmissionInquiryModel(models.Model):
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    date_of_birth = models.CharField(max_length=20)
    entering_grade = models.CharField(max_length=30)
    year_applying = models.CharField(max_length=20)
    current_school = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    home_phone = models.CharField(max_length=10)
    relation = models.CharField(max_length=50)
    prefix = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    hear_about_school = models.CharField(max_length=100, blank=True)
    additional_query = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)


class GalleryModel(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="image/collection/")
