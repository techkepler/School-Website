from pkgutil import get_data
from rest_framework import serializers
from studentApi.models import (
    StudentAbsentModel,
    StudentAttendanceModel,
    StudentDataCollection,
    StudentFeeModel,
    StudentFeePaymentModel,
    StudentResultCollectionModel,
)
from django.forms import ValidationError
import pandas as pd
from datetime import date


class StudentCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDataCollection
        fields = "__all__"


class StudentRegisterExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_Student = StudentDataCollection.objects.filter(id=datas.get("Id"))
            check_email = StudentDataCollection.objects.filter(email=datas.get("Email"))
            if check_Student.exists():
                raise ValidationError(
                    "Student with "
                    + "ID: "
                    + str(datas.get("Id"))
                    + " already exist in system"
                )
            elif check_email.exists():
                raise ValidationError(
                    "Student with email "
                    + datas.get("Email")
                    + " already exist in system."
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_student = []
        for datas in csvData:
            student = StudentDataCollection(
                id=datas.get("Id"),
                name=datas.get("Name"),
                email=datas.get("Email"),
                phone=datas.get("Phone Number"),
                gender=datas.get("Gender"),
                grade=datas.get("Grade"),
                address=datas.get("Address"),
                date=date.today(),
            )
            collect_student.append(student)
        return StudentDataCollection.objects.bulk_create(collect_student)


class StudentGradeUpdateSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = str(attrs.get("date")).split("-")
        get_stu = StudentDataCollection.objects.all().order_by("grade")

        for stu in get_stu:
            get_date = str(stu.date).split("-")
            if get_date[0] == grab_date[0]:
                raise ValidationError("You can't update the student grade yet.")
        return super().validate(attrs)

    def create(self, validated_data):
        get_stu = StudentDataCollection.objects.all().order_by("grade")
        grab_date = validated_data.get("date")

        for stu in get_stu:
            if stu.grade == "Twelve":
                stu.delete()
                stu.save()
            else:
                if stu.grade == "Nursery" and stu.date != grab_date:
                    stu.grade = "L.K.G"
                    stu.date = grab_date

                if stu.grade == "L.K.G" and stu.date != grab_date:
                    stu.grade = "U.K.G"
                    stu.date = grab_date

                if stu.grade == "U.K.G" and stu.date != grab_date:
                    stu.grade = "One"
                    stu.date = grab_date

                if stu.grade == "One" and stu.date != grab_date:
                    stu.grade = "Two"
                    stu.date = grab_date

                if stu.grade == "Two" and stu.date != grab_date:
                    stu.grade = "Three"
                    stu.date = grab_date

                if stu.grade == "Three" and stu.date != grab_date:
                    stu.grade = "Four"
                    stu.date = grab_date

                if stu.grade == "Four" and stu.date != grab_date:
                    stu.grade = "Five"
                    stu.date = grab_date

                if stu.grade == "Five" and stu.date != grab_date:
                    stu.grade = "Six"
                    stu.date = grab_date

                if stu.grade == "Six" and stu.date != grab_date:
                    stu.grade = "Seven"
                    stu.date = grab_date

                if stu.grade == "Seven" and stu.date != grab_date:
                    stu.grade = "Eight"
                    stu.date = grab_date

                if stu.grade == "Eight" and stu.date != grab_date:
                    stu.grade = "Nine"
                    stu.date = grab_date

                if stu.grade == "Nine" and stu.date != grab_date:
                    stu.grade = "Ten"
                    stu.date = grab_date

                if stu.grade == "Ten" and stu.date != grab_date:
                    stu.grade = "Eleven"
                    stu.date = grab_date

                if stu.grade == "Eleven" and stu.date != grab_date:
                    stu.grade = "Twelve"
                    stu.date = grab_date

            stu.save()

        return validated_data


# ...................Student Attendance Serializers..................


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendanceModel
        fields = "__all__"

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        attend_day = validated_data.get("attend_day")
        absent_day = validated_data.get("absent_day")
        total_day = validated_data.get("total_day")
        date = validated_data.get("date")

        StudentAttendanceModel.objects.create(
            id=grab_id,
            attend_day=attend_day,
            absent_day=absent_day,
            total_day=total_day,
            date=date,
            name=grab_id.name,
            grade=grab_id.grade,
        )
        return validated_data


class StudentAttendanceExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_Student = StudentDataCollection.objects.filter(id=datas.get("id"))
            if not check_Student.exists():
                raise ValidationError(
                    "Student with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " doesn't exist in system"
                )
            elif StudentAttendanceModel.objects.filter(id=datas.get("id")).exists():
                raise ValidationError(
                    "Student with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " Already Exist in Student Attendance."
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_attendance = []
        for datas in csvData:
            get_student = StudentDataCollection.objects.get(id=datas.get("id"))
            attendance = StudentAttendanceModel(
                id=get_student,
                attend_day=datas.get("attend_day"),
                absent_day=datas.get("absent_day"),
                total_day=int(datas.get("attend_day")) + int(datas.get("absent_day")),
                date=date.today(),
            )
            collect_attendance.append(attendance)
        return StudentAttendanceModel.objects.bulk_create(collect_attendance)


class UpdateAttendanceSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = attrs.get("date")
        attendance = StudentAttendanceModel.objects.all()
        for attend in attendance:
            if attend.date == grab_date:
                raise ValidationError(
                    "Student Attendance for Today has already been updated."
                )
        return super().validate(attrs)

    def create(self, validated_data):
        attendance = StudentAttendanceModel.objects.all()
        grab_date = validated_data.get("date")
        for attend in attendance:
            attend.attend_day = int(attend.attend_day) + 1
            attend.total_day = int(attend.attend_day) + int(attend.absent_day)
            attend.date = grab_date
            attend.save()
        return validated_data


class UpdateAbsentSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    date = serializers.DateField()

    class Meta:
        fields = ["id", "date"]

    def validate(self, attrs):
        grab_id = attrs.get("id")
        grab_date = attrs.get("date")
        attendance = StudentAttendanceModel.objects.filter(id=grab_id)
        absent = StudentAbsentModel.objects.filter(student_details=grab_id)

        if not attendance.exists():
            raise ValidationError(
                "Student with given ID doesn't exist in Student Attendance Model yet."
            )

        elif absent.exists():
            for absents in absent:
                if absents.date == grab_date:
                    raise ValidationError(
                        "Absent for given Student ID has already been updated for today."
                    )

        return super().validate(attrs)

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        grab_date = validated_data.get("date")
        absent = StudentAttendanceModel.objects.get(id=grab_id)
        if int(absent.attend_day) >= 1:
            absent.absent_day = int(absent.absent_day) + 1
            absent.attend_day = int(absent.attend_day) - 1
            absent.total_day = int(absent.attend_day) + int(absent.absent_day)
        else:
            absent.absent_day = int(absent.absent_day) + 1
            absent.attend_day = 0
            absent.total_day = int(absent.attend_day) + int(absent.absent_day)
        absent.save()
        absent_date = StudentAbsentModel.objects.create(
            student_details=absent.id, name=absent.name, date=grab_date
        )
        absent_date.save()

        return validated_data


class AttendanceResetSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def create(self, validated_data):
        date = validated_data.get("date")
        get_attendance = StudentAttendanceModel.objects.all()
        absent_collection = StudentAbsentModel.objects.all()

        for absent in absent_collection:
            absent.delete()

        for attend in get_attendance:
            get_stu = attend.id
            attend.absent_day = 0
            attend.attend_day = 0
            attend.total_day = 0
            attend.grade = get_stu.grade
            attend.date = date
            attend.save()
        return validated_data


class StudentAbsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAbsentModel
        fields = "__all__"


# # ........................Student Fee Serializer ................


class StudentFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFeeModel
        fields = "__all__"

    def create(self, validated_data):
        grab_id = validated_data.get("id")
        monthly_fee = validated_data.get("monthly_fee")
        computer_fee = validated_data.get("computer_fee")
        bus_fee = validated_data.get("bus_fee")
        paid_fee = validated_data.get("paid_fee")
        unpaid_fee = validated_data.get("unpaid_fee")
        total_fee = validated_data.get("total_fee")
        date = validated_data.get("date")
        StudentFeeModel.objects.create(
            id=grab_id,
            name=grab_id.name,
            grade=grab_id.grade,
            monthly_fee=monthly_fee,
            computer_fee=computer_fee,
            bus_fee=bus_fee,
            paid_fee=paid_fee,
            unpaid_fee=unpaid_fee,
            total_fee=total_fee,
            date=date,
        )
        return validated_data


class StudentFeeExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_Student = StudentDataCollection.objects.filter(id=datas.get("ID"))
            if not check_Student.exists():
                raise ValidationError(
                    "Student with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " doesn't exist in system"
                )
            elif StudentFeeModel.objects.filter(id=datas.get("ID")).exists():
                raise ValidationError(
                    "Student with "
                    + "ID: "
                    + str(datas.get("ID"))
                    + " Already Exist in Student Fee Model."
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_attendance = []
        for datas in csvData:
            paid_fee = datas.get("Paid Fee")
            total_fee = datas.get("Total Fee")
            if int(paid_fee) <= int(total_fee):
                unpaid_fee = int(total_fee) - int(paid_fee)
            else:
                unpaid_fee = 0

            get_student = StudentDataCollection.objects.get(id=datas.get("ID"))
            attendance = StudentFeeModel(
                id=get_student,
                monthly_fee=datas.get("Monthly Fee"),
                computer_fee=datas.get("Computer Fee"),
                bus_fee=datas.get("Bus Fee"),
                paid_fee=paid_fee,
                unpaid_fee=unpaid_fee,
                total_fee=total_fee,
                name=get_student.name,
                date=date.today(),
            )
            collect_attendance.append(attendance)
        return StudentFeeModel.objects.bulk_create(collect_attendance)


class UpdateFeeSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def validate(self, attrs):
        grab_date = str(attrs.get("date")).split("-")
        fee = StudentFeeModel.objects.all()
        for fees in fee:
            date = str(fees.date).split("-")
            if date[1] == grab_date[1]:
                raise ValidationError(
                    "Student Fee for this Month has already been updated."
                )
        return super().validate(attrs)

    def create(self, validated_data):
        fee = StudentFeeModel.objects.all()
        grab_date = validated_data.get("date")
        for fees in fee:
            fees.total_fee = (
                int(fees.total_fee)
                + int(fees.monthly_fee)
                + int(fees.computer_fee)
                + int(fees.bus_fee)
            )
            if int(fees.total_fee) >= int(fees.paid_fee):
                fees.unpaid_fee = int(fees.total_fee) - int(fees.paid_fee)
            else:
                fees.unpaid_fee = 0
            fees.date = grab_date
            fees.save()
        return validated_data


class StudentFeePaymentSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=20)
    amount = serializers.CharField(max_length=10)
    date = serializers.DateField()

    class Meta:
        fields = ["id", "amount", "date"]

    def validate(self, attrs):
        grab_id = attrs.get("id")
        print(type(grab_id))
        check_Student = StudentFeeModel.objects.filter(id=grab_id)
        if not check_Student.exists():
            raise ValidationError(
                "Given Student ID hasn't been registered  in Student Fee Model yet."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        id = validated_data.get("id")
        amount = validated_data.get("amount")
        date = validated_data.get("date")
        get_student = StudentFeeModel.objects.get(id=id)
        get_student.paid_fee = int(get_student.paid_fee) + int(amount)
        if int(get_student.total_fee) >= int(get_student.paid_fee):
            get_student.unpaid_fee = int(get_student.total_fee) - int(
                get_student.paid_fee
            )
        else:
            get_student.unpaid_fee = 0
        get_student.save()

        StudentFeePaymentModel.objects.create(
            student_details=get_student.id,
            name=get_student.name,
            amount=amount,
            date=date,
        )
        return validated_data


class FeeResetSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ["date"]

    def create(self, validated_data):
        date = validated_data.get("date")
        get_fee = StudentFeeModel.objects.all()
        fee_collection = StudentFeePaymentModel.objects.all()
        for fees in fee_collection:
            fees.delete()

        for fee in get_fee:
            get_stu = fee.id
            fee.paid_fee = 0
            fee.total_fee = 0
            fee.grade = get_stu.grade
            fee.date = date
            fee.save()
        return validated_data


# Student Result Serializer


class StudentResutlSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = StudentResultCollectionModel

    def validate(self, attrs):
        id = attrs.get("stu_details")
        sub = attrs.get("subject")
        exam_term = attrs.get("exam_term")
        get_result = StudentResultCollectionModel.objects.filter(stu_details=id)
        if get_result.exists():
            for result in get_result:
                if result.subject == sub and result.exam_term == exam_term:
                    raise ValidationError(
                        sub
                        + " subject result already exist for "
                        + exam_term
                        + " exam."
                    )
        return attrs

    def create(self, validated_data):
        stu_details = validated_data.get("stu_details")
        sub = validated_data.get("subject")
        exam_term = validated_data.get("exam_term")
        total_marks = validated_data.get("total_marks")
        pass_marks = validated_data.get("pass_marks")
        obtained_marks = validated_data.get("obtained_marks")
        gpa = validated_data.get("gpa")

        return StudentResultCollectionModel.objects.create(
            stu_details=stu_details,
            name=stu_details.name,
            subject=sub,
            total_marks=total_marks,
            pass_marks=pass_marks,
            obtained_marks=obtained_marks,
            exam_term=exam_term,
            gpa=gpa,
            grade=stu_details.grade,
        )


class StudentResultExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_Student = StudentDataCollection.objects.filter(id=datas.get("ID"))
            if not check_Student.exists():
                raise ValidationError(
                    "Student with "
                    + "ID: "
                    + str(datas.get("id"))
                    + " doesn't exist in system"
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_attendance = []
        for datas in csvData:
            id = datas.get("Student Id")
            name = datas.get("Name")
            grade = datas.get("Grade")
            paid_fee = datas.get("Paid Fee")
            total_fee = datas.get("Total Fee")
            if int(paid_fee) <= int(total_fee):
                unpaid_fee = int(total_fee) - int(paid_fee)
            else:
                unpaid_fee = 0

            get_student = StudentDataCollection.objects.get(id=datas.get("ID"))
            attendance = StudentFeeModel(
                id=get_student,
                monthly_fee=datas.get("Monthly Fee"),
                computer_fee=datas.get("Computer Fee"),
                bus_fee=datas.get("Bus Fee"),
                paid_fee=paid_fee,
                unpaid_fee=unpaid_fee,
                total_fee=total_fee,
                name=get_student.name,
                date=date.today(),
            )
            collect_attendance.append(attendance)
        return StudentFeeModel.objects.bulk_create(collect_attendance)
