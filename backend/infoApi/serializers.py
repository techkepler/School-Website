from rest_framework import serializers
from django.forms import ValidationError
import pandas as pd

from .models import (
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


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = AnnouncementModel


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = NewsModel


class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = BlogModel


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = EventsModel


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CalendarEventModel


class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = LeaveApplicationModel

    def validate(self, attrs):
        grab_date = attrs.get("date")
        grab_id = attrs.get("stu_id")
        check_stu = LeaveApplicationModel.objects.filter(stu_id=grab_id)
        if check_stu.exists():
            for stu in check_stu:
                if stu.date == grab_date:
                    raise ValidationError(
                        "You can't submit two leave application form on same day."
                    )
        return super().validate(attrs)

    def create(self, validated_data):
        stu = validated_data.get("stu_id")
        name = validated_data.get("name")
        grade = validated_data.get("grade")
        reason = validated_data.get("reason")
        status = validated_data.get("status")
        date = validated_data.get("date")

        return LeaveApplicationModel.objects.create(
            stu_id=stu,
            name=name,
            grade=grade,
            reason=reason,
            status=status,
            date=date,
        )


class AdmissionInquirySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = AdmissionInquiryModel


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = GalleryModel


class RoutinesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = RoutineModel

    def validate(self, attrs):
        subject = attrs.get("subject")
        grade = attrs.get("grade")
        exam_term = attrs.get("exam_term")
        get_routine = RoutineModel.objects.filter(grade=grade)
        if get_routine.exists():
            for routine in get_routine:
                if routine.subject == subject and routine.exam_term == exam_term:
                    raise ValidationError(
                        subject
                        + " Subject Routine for "
                        + exam_term
                        + " examination of grade "
                        + grade
                        + " already exist."
                    )

        return attrs


class RoutineExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            grade = datas.get("Grade")
            subject = datas.get("Subject")
            exam_term = datas.get("Exam Term")
            get_routine = RoutineModel.objects.filter(grade=grade)
            if get_routine.exists():
                for routine in get_routine:
                    if routine.subject == subject and routine.exam_term == exam_term:
                        raise ValidationError(
                            subject
                            + " Subject Routine for "
                            + exam_term
                            + " examination of grade "
                            + grade
                            + " already exist."
                        )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_routine = []
        for datas in csvData:
            routine = RoutineModel(
                grade=datas.get("Grade"),
                subject=datas.get("Subject"),
                date=datas.get("Date"),
                start_time=datas.get("Start Time"),
                end_time=datas.get("End Time"),
                exam_term=datas.get("Exam Term"),
            )

            collect_routine.append(routine)
        return RoutineModel.objects.bulk_create(collect_routine)
