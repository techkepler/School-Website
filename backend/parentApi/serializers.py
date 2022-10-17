from rest_framework import serializers
from django.forms import ValidationError
from .models import ParentDataCollection
import pandas as pd


class ParentCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = ParentDataCollection


class ParentRegisterExcleFileSerializer(serializers.Serializer):
    file_data = serializers.FileField()

    class Meta:
        fields = ["file_data"]

    def validate(self, attrs):
        get_file = attrs.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        for datas in csvData:
            check_parent = ParentDataCollection.objects.filter(id=datas.get("Id"))
            check_email = ParentDataCollection.objects.filter(email=datas.get("Email"))
            if check_parent.exists():
                raise ValidationError(
                    "Parent with "
                    + "ID: "
                    + str(datas.get("Id"))
                    + " already exist in system"
                )
            elif check_email.exists():
                raise ValidationError(
                    "Parent with email "
                    + datas.get("Email")
                    + " already exist in system."
                )

        return super().validate(attrs)

    def create(self, validated_data):
        get_file = validated_data.get("file_data")
        exceldata = pd.read_excel(get_file)
        csvData = exceldata.to_dict(orient="records")
        collect_parent = []
        for datas in csvData:
            parent = ParentDataCollection(
                id=datas.get("Id"),
                name=datas.get("Name"),
                email=datas.get("Email"),
                phone=datas.get("Phone"),
                address=datas.get("Address"),
            )
            collect_parent.append(parent)
        return ParentDataCollection.objects.bulk_create(collect_parent)
