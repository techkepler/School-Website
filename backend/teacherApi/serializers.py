from termios import VLNEXT
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from teacherApi.models import (
    HomeworkModel,
    TeacherAbsentModel,
    TeacherAttendanceModel,
    TeacherDataCollection,
    TeacherSalaryModel,
    TeacherSalaryPaymentModel,
)
from django.forms import ValidationError
import pandas as pd
from datetime import date


class TeacherCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherDataCollection
        fields = "__all__"


# ...................Teacher Attendance Serializers..................


class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendanceModel
        fields = "__all__"

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        attend_day = validated_data.get("attend_day")
        absent_day = validated_data.get("absent_day")
        total_day = validated_data.get("total_day")
        date = validated_data.get("date")

        TeacherAttendanceModel.objects.create(
            id=grab_id,
            attend_day=attend_day,
            absent_day=absent_day,
            total_day=total_day,
            date=date,
            name=grab_id.name,
        )
        return validated_data


class TeacherAttendanceExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_teacher = TeacherDataCollection.objects.filter(id=datas.get("id"))
            if not check_teacher.exists():
                raise ValidationError(
                    "Teacher with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " doesn't exist in system"
                )
            elif TeacherAttendanceModel.objects.filter(id=datas.get("id")).exists():
                raise ValidationError(
                    "Teacher with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " Already Exist in Teacher Attendance."
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_attendance = []
        for datas in csvData:
            get_teacher = TeacherDataCollection.objects.get(id=datas.get("id"))
            attendance = TeacherAttendanceModel(
                id=get_teacher,
                attend_day=datas.get("attend_day"),
                absent_day=datas.get("absent_day"),
                total_day=int(datas.get("attend_day")) + int(datas.get("absent_day")),
                date=date.today(),
            )
            collect_attendance.append(attendance)
        return TeacherAttendanceModel.objects.bulk_create(collect_attendance)


class UpdateAttendanceSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = attrs.get("date")
        attendance = TeacherAttendanceModel.objects.all()
        for attend in attendance:
            if attend.date == grab_date:
                raise ValidationError(
                    "Teacher Attendance for Today has already been updated."
                )
        return super().validate(attrs)

    def create(self, validated_data):
        attendance = TeacherAttendanceModel.objects.all()
        grab_date = validated_data.get("date")
        for attend in attendance:
            attend.attend_day = int(attend.attend_day) + 1
            attend.total_day = int(attend.attend_day) + int(attend.absent_day)
            attend.date = grab_date
            attend.save()
        return validated_data


class UpdateAbsentSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=20)
    date = serializers.DateField()

    class Meta:
        fields = ["id" "date"]

    def validate(self, attrs):
        grab_id = attrs.get("id")
        grab_date = attrs.get("date")
        attendance = TeacherAttendanceModel.objects.filter(id=grab_id)
        absent = TeacherAbsentModel.objects.filter(teacher_details=grab_id)
        if not attendance.exists():
            raise ValidationError(
                "Teacher with this ID doesn't exist in Teacher Attendance Model yet."
            )
        elif absent.exists():
            for absents in absent:
                if absents.date == grab_date:
                    raise ValidationError(
                        "Absent for given teacher ID has already been updated for today."
                    )

        return super().validate(attrs)

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        grab_date = validated_data.get("date")
        attendance = TeacherAttendanceModel.objects.get(id=grab_id)
        if int(attendance.attend_day) >= 1:
            attendance.absent_day = int(attendance.absent_day) + 1
            attendance.attend_day = int(attendance.attend_day) - 1
            attendance.total_day = int(attendance.attend_day) + int(
                attendance.absent_day
            )
        else:
            attendance.absent_day = int(attendance.absent_day) + 1
            attendance.attend_day = 0
            attendance.total_day = int(attendance.attend_day) + int(
                attendance.absent_day
            )
        attendance.save()
        TeacherAbsentModel.objects.create(
            teacher_details=attendance.id, name=attendance.name, date=grab_date
        )

        return validated_data


class AttendanceResetSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = str(attrs.get("date")).split("-")
        get_attendance = TeacherAttendanceModel.objects.all()
        for attend in get_attendance:
            if str(attend.date).split("-")[0] == grab_date[0]:
                raise ValidationError(
                    "You can't reset the teacher attendance model yet."
                )
        return super().validate(attrs)

    def create(self, validated_data):
        date = validated_data.get("date")
        get_attendance = TeacherAttendanceModel.objects.all()
        for attend in get_attendance:
            attend.absent_day = 0
            attend.attend_day = 0
            attend.total_day = 0
            attend.date = date
            attend.save()
        return validated_data


# ........................Teacher Salary Serializer ................


class TeacherSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSalaryModel
        fields = "__all__"

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        monthly_salary = validated_data.get("monthly_salary")
        paid_salary = validated_data.get("paid_salary")
        total_salary = validated_data.get("total_salary")
        date = validated_data.get("date")
        unpaid_salary = int(total_salary) - int(paid_salary)

        TeacherSalaryModel.objects.create(
            id=grab_id,
            monthly_salary=monthly_salary,
            paid_salary=paid_salary,
            unpaid_salary=unpaid_salary,
            total_salary=total_salary,
            date=date,
            name=grab_id.name,
        )
        return validated_data


class TeacherSalaryExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_teacher = TeacherDataCollection.objects.filter(id=datas.get("id"))
            if not check_teacher.exists():
                raise ValidationError(
                    "Teacher with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " doesn't exist in system"
                )
            elif TeacherSalaryModel.objects.filter(id=datas.get("id")).exists():
                raise ValidationError(
                    "Teacher with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " Already Exist in Teacher Salary."
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_attendance = []
        for datas in csvData:
            paid_salary = datas.get("paid_salary")
            total_salary = datas.get("total_salary")
            unpaid_salary = int(total_salary) - int(paid_salary)
            get_teacher = TeacherDataCollection.objects.get(id=datas.get("id"))
            attendance = TeacherSalaryModel(
                id=get_teacher,
                monthly_salary=datas.get("monthly_salary"),
                paid_salary=paid_salary,
                unpaid_salary=unpaid_salary,
                total_salary=total_salary,
                name=get_teacher.name,
                date=date.today(),
            )
            collect_attendance.append(attendance)
        return TeacherSalaryModel.objects.bulk_create(collect_attendance)


class UpdateSalarySerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = str(attrs.get("date")).split("-")
        salary = TeacherSalaryModel.objects.all()
        for salarys in salary:
            date = str(salarys.date).split("-")
            if date[1] == grab_date[1]:
                raise ValidationError(
                    "Teacher Salary for this Month has already been updated."
                )
        return super().validate(attrs)

    def create(self, validated_data):
        salary = TeacherSalaryModel.objects.all()
        grab_date = validated_data.get("date")
        for salarys in salary:
            salarys.total_salary = int(salarys.total_salary) + int(
                salarys.monthly_salary
            )
            salarys.unpaid_salary = int(salarys.total_salary) - int(salarys.paid_salary)
            salarys.date = grab_date
            salarys.save()
        return validated_data


class TeacherSalaryPaymentSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=20)
    amount = serializers.CharField(max_length=10)
    date = serializers.DateField()

    class Meta:
        fields = ["id", "amount", "date"]

    def validate(self, attrs):
        grab_id = attrs.get("id")
        print(type(grab_id))
        check_teacher = TeacherSalaryModel.objects.filter(id=grab_id)
        if not check_teacher.exists():
            raise ValidationError(
                "Given Teacher ID hasn't been registered  in Teacher Salary Model yet."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        id = validated_data.get("id")
        amount = validated_data.get("amount")
        date = validated_data.get("date")
        get_teacher = TeacherSalaryModel.objects.get(id=id)
        get_teacher.paid_salary = int(get_teacher.paid_salary) + int(amount)
        get_teacher.unpaid_salary = int(get_teacher.total_salary) - int(
            get_teacher.paid_salary
        )
        get_teacher.save()
        TeacherSalaryPaymentModel.objects.create(
            teacher_details=get_teacher.id,
            name=get_teacher.name,
            amount=amount,
            date=date,
        )
        return validated_data


class SalaryResetSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = str(attrs.get("date")).split("-")
        get_salary = TeacherSalaryModel.objects.all()
        for salary in get_salary:
            if str(salary.date).split("-")[0] == grab_date[0]:
                raise ValidationError("You can't reset the teacher salary model yet.")
        return super().validate(attrs)

    def create(self, validated_data):
        date = validated_data.get("date")
        get_salary = TeacherSalaryModel.objects.all()
        for salary in get_salary:
            salary.paid_salary = 0
            salary.total_salary = 0
            salary.date = date
            salary.save()
        return validated_data


# Homework Serializers
class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkModel
        fields = "__all__"

    def validate(self, attrs):
        grab_sub = attrs.get("subject")
        grab_date = attrs.get("date")
        grab_grade = attrs.get("grade")
        homework = HomeworkModel.objects.filter(grade=grab_grade)

        for homeworks in homework:
            if homeworks.subject == grab_sub and homeworks.date == grab_date:
                raise ValidationError("Grade " + grab_grade + " " + grab_sub + " subject homework already exist for today.")

        return super().validate(attrs)
