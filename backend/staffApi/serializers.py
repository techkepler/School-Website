from rest_framework import serializers
from staffApi.models import (
    StaffAbsentModel,
    StaffDataCollection,
    StaffAttendanceModel,
    StaffSalaryModel,
    StaffSalaryPaymentModel,
)
from django.forms import ValidationError
import pandas as pd
from datetime import date


class StaffCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDataCollection
        fields = "__all__"


# ...................staff Attendance Serializers..................


class StaffAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendanceModel
        fields = "__all__"

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        attend_day = validated_data.get("attend_day")
        absent_day = validated_data.get("absent_day")
        total_day = validated_data.get("total_day")
        date = validated_data.get("date")

        StaffAttendanceModel.objects.create(
            id=grab_id,
            attend_day=attend_day,
            absent_day=absent_day,
            total_day=total_day,
            date=date,
            name=grab_id.name,
        )
        return validated_data


class StaffAttendanceExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_staff = StaffDataCollection.objects.filter(id=datas.get("id"))
            if not check_staff.exists():
                raise ValidationError(
                    "Staff with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " doesn't exist in system"
                )
            elif StaffAttendanceModel.objects.filter(id=datas.get("id")).exists():
                raise ValidationError(
                    "Staff with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " Already Exist in Staff Attendance."
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_attendance = []
        for datas in csvData:
            get_staff = StaffDataCollection.objects.get(id=datas.get("id"))
            attendance = StaffAttendanceModel(
                id=get_staff,
                attend_day=datas.get("attend_day"),
                absent_day=datas.get("absent_day"),
                total_day=int(datas.get("attend_day")) + int(datas.get("absent_day")),
                date=date.today(),
            )
            collect_attendance.append(attendance)
        return StaffAttendanceModel.objects.bulk_create(collect_attendance)


class UpdateAttendanceSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = attrs.get("date")
        attendance = StaffAttendanceModel.objects.all()
        for attend in attendance:
            if attend.date == grab_date:
                raise ValidationError(
                    "staff Attendance for Today has already been updated."
                )
        return super().validate(attrs)

    def create(self, validated_data):
        attendance = StaffAttendanceModel.objects.all()
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
        fields = ["id", "date"]

    def validate(self, attrs):
        grab_id = attrs.get("id")
        grab_date = attrs.get("date")
        attendance = StaffAttendanceModel.objects.filter(id=grab_id)
        absent = StaffAbsentModel.objects.filter(staff_details=grab_id)

        if not attendance.exists():
            raise ValidationError(
                "Staff with given ID doesn't exist in Staff Attendance Model yet."
            )

        elif absent.exists():
            for absents in absent:
                if absents.date == grab_date:
                    raise ValidationError(
                        "Absent for given staff ID has already been updated for today."
                    )

        return super().validate(attrs)

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        grab_date = validated_data.get("date")
        absent = StaffAttendanceModel.objects.get(id=grab_id)
        if int(absent.attend_day) >= 1:
            absent.absent_day = int(absent.absent_day) + 1
            absent.attend_day = int(absent.attend_day) - 1
            absent.total_day = int(absent.attend_day) + int(absent.absent_day)
        else:
            absent.absent_day = int(absent.absent_day) + 1
            absent.attend_day = 0
            absent.total_day = int(absent.attend_day) + int(absent.absent_day)
        absent.save()
        StaffAbsentModel.objects.create(
            staff_details=absent.id, name=absent.name, date=grab_date
        )

        return validated_data


class AttendanceResetSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = str(attrs.get("date")).split("-")
        get_attendance = StaffAttendanceModel.objects.all()
        for attend in get_attendance:
            if str(attend.date).split("-")[0] == grab_date[0]:
                raise ValidationError("You can't reset the staff attendance model yet.")
        return super().validate(attrs)

    def create(self, validated_data):
        date = validated_data.get("date")
        get_attendance = StaffAttendanceModel.objects.all()
        for attend in get_attendance:
            attend.absent_day = 0
            attend.attend_day = 0
            attend.total_day = 0
            attend.date = date
            attend.save()
        return validated_data


# ........................Staff Salary Serializer ................


class StaffSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSalaryModel
        fields = "__all__"

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        monthly_salary = validated_data.get("monthly_salary")
        paid_salary = validated_data.get("paid_salary")
        total_salary = validated_data.get("total_salary")
        date = validated_data.get("date")
        unpaid_salary = int(total_salary) - int(paid_salary)

        StaffSalaryModel.objects.create(
            id=grab_id,
            monthly_salary=monthly_salary,
            paid_salary=paid_salary,
            unpaid_salary=unpaid_salary,
            total_salary=total_salary,
            date=date,
            name=grab_id.name,
        )
        return validated_data


class StaffSalaryExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_staff = StaffDataCollection.objects.filter(id=datas.get("id"))
            if not check_staff.exists():
                raise ValidationError(
                    "Staff with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " doesn't exist in system"
                )
            elif StaffSalaryModel.objects.filter(id=datas.get("id")).exists():
                raise ValidationError(
                    "Staff with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " Already Exist in staff Salary."
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

            get_staff = StaffSalaryModel.objects.get(id=datas.get("id"))
            attendance = StaffSalaryModel(
                id=get_staff,
                monthly_salary=datas.get("monthly_salary"),
                paid_salary=paid_salary,
                unpaid_salary=unpaid_salary,
                total_salary=total_salary,
                name=get_staff.name,
                date=date.today(),
            )
            collect_attendance.append(attendance)
        return StaffSalaryModel.objects.bulk_create(collect_attendance)


class UpdateSalarySerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = str(attrs.get("date")).split("-")
        salary = StaffSalaryModel.objects.all()
        for salarys in salary:
            date = str(salarys.date).split("-")
            if date[1] == grab_date[1]:
                raise ValidationError(
                    "Staff Salary for this Month has already been updated."
                )
        return super().validate(attrs)

    def create(self, validated_data):
        salary = StaffSalaryModel.objects.all()
        grab_date = validated_data.get("date")
        for salarys in salary:
            salarys.total_salary = int(salarys.total_salary) + int(
                salarys.monthly_salary
            )
            salarys.unpaid_salary = int(salarys.total_salary) - int(salarys.paid_salary)
            salarys.date = grab_date
            salarys.save()
        return validated_data


class StaffSalaryPaymentSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=20)
    amount = serializers.CharField(max_length=10)
    date = serializers.DateField()

    class Meta:
        fields = ["id", "amount", "date"]

    def validate(self, attrs):
        grab_id = attrs.get("id")
        print(type(grab_id))
        check_staff = StaffSalaryModel.objects.filter(id=grab_id)
        if not check_staff.exists():
            raise ValidationError(
                "Given Staff ID hasn't been registered  in staff Salary Model yet."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        id = validated_data.get("id")
        print(type(id))
        amount = validated_data.get("amount")
        date = validated_data.get("date")
        print(date)
        get_staff = StaffSalaryModel.objects.get(id=id)
        get_staff.paid_salary = int(get_staff.paid_salary) + int(amount)
        get_staff.unpaid_salary = int(get_staff.total_salary) - int(
            get_staff.paid_salary
        )
        get_staff.save()
        StaffSalaryPaymentModel.objects.create(
            staff_details=get_staff.id,
            name=get_staff.name,
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
        get_salary = StaffSalaryModel.objects.all()
        for salary in get_salary:
            if str(salary.date).split("-")[0] == grab_date[0]:
                raise ValidationError("You can't reset the staff salary model yet.")
        return super().validate(attrs)

    def create(self, validated_data):
        date = validated_data.get("date")
        get_salary = StaffSalaryModel.objects.all()
        for salary in get_salary:
            salary.paid_salary = 0
            salary.total_salary = 0
            salary.date = date
            salary.save()
        return validated_data
