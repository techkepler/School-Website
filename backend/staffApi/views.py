from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from AdminPanel.renderers import ErrorRenderer
from staffApi.serializers import (
    AttendanceResetSerializer,
    SalaryResetSerializer,
    StaffAttendanceExcleFileSerializer,
    StaffAttendanceSerializer,
    StaffCRUDSerializer,
    StaffSalaryExcleFileSerializer,
    StaffSalaryPaymentSerializer,
    StaffSalarySerializer,
    UpdateAttendanceSerializer,
    UpdateAbsentSerializer,
    UpdateSalarySerializer,
)
from .models import StaffAttendanceModel, StaffDataCollection, StaffSalaryModel


class CustomPagination(PageNumberPagination):
    page_size = 5


# Staff CRUD VIEWS


class CRUDStaffViewAdmin(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StaffCRUDSerializer
    queryset = StaffDataCollection.objects.all().order_by("name")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id"]


class CRUDStaffViewPublic(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StaffCRUDSerializer
    queryset = StaffDataCollection.objects.all().order_by("name")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id"]


# ...................Staff Attendance Views..........................


class StaffAttendanceCRUDPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StaffAttendanceSerializer
    queryset = StaffAttendanceModel.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class StaffAttendanceRegisterView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StaffAttendanceSerializer
    queryset = StaffAttendanceModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class StaffAttendanceRegisterExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StaffAttendanceExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StaffUpdateAttendanceView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateAttendanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StaffAbsentUpdateView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateAbsentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class ResetStaffAttendanceView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = AttendanceResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors)


# ........... Staff Salary View ..............


class StaffSalaryCRUDPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StaffSalarySerializer
    queryset = StaffSalaryModel.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class StaffSalaryView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StaffSalarySerializer
    queryset = StaffSalaryModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class StaffSalaryExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StaffSalaryExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StaffUpdateSalaryView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateSalarySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StaffSalaryPaymentView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StaffSalaryPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StaffSalaryPaymentStoreView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StaffSalaryPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class ResetStaffSalaryView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = SalaryResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors)
