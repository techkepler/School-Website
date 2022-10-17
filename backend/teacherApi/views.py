from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from AdminPanel.renderers import ErrorRenderer
from teacherApi.serializers import (
    AttendanceResetSerializer,
    HomeworkSerializer,
    SalaryResetSerializer,
    TeacherAttendanceExcleFileSerializer,
    TeacherAttendanceSerializer,
    TeacherCRUDSerializer,
    TeacherSalaryExcleFileSerializer,
    TeacherSalaryPaymentSerializer,
    TeacherSalarySerializer,
    UpdateAttendanceSerializer,
    UpdateAbsentSerializer,
    UpdateSalarySerializer,
)
from .models import (
    HomeworkModel,
    TeacherAbsentModel,
    TeacherAttendanceModel,
    TeacherDataCollection,
    TeacherSalaryModel,
    TeacherSalaryPaymentModel,
)


class CustomPagination(PageNumberPagination):
    page_size = 10


# Teacher CRUD VIEWS


class CRUDTeacherViewAdmin(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = TeacherCRUDSerializer
    queryset = TeacherDataCollection.objects.all().order_by("name")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id"]


class CRUDTeacherViewPublic(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = TeacherCRUDSerializer
    queryset = TeacherDataCollection.objects.all().order_by("name")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id"]


# ...................Teacher Attendance Views..........................


class TeacherAttendanceCRUDPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = TeacherAttendanceSerializer
    queryset = TeacherAttendanceModel.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class TeacherAttendanceRegisterView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = TeacherAttendanceSerializer
    queryset = TeacherAttendanceModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class TeacherAttendanceRegisterExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = TeacherAttendanceExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class TeacherUpdateAttendanceView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateAttendanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class TeacherAbsentUpdateView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateAbsentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class TeacherAbsentStoreView(APIView):
    renderer_classes = [ErrorRenderer]
    serializer_class = UpdateAbsentSerializer
    queryset = TeacherAbsentModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class ResetTeacherAttendanceView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = AttendanceResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors)


# ........... Teacher Salary View ..............


class TeacherSalaryCRUDPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = TeacherSalarySerializer
    queryset = TeacherSalaryModel.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class TeacherSalaryView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = TeacherSalarySerializer
    queryset = TeacherSalaryModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["teacher_details", "name"]


class TeacherSalaryExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = TeacherSalaryExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class TeacherUpdateSalaryView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateSalarySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class TeacherSalaryPaymentView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = TeacherSalaryPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class TeacherSalaryPaymentStoreView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = TeacherSalaryPaymentSerializer
    queryset = TeacherSalaryPaymentModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["teacher_details", "name"]


class ResetTeacherSalaryView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = SalaryResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors)


class HomeWorkView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = HomeworkSerializer
    queryset = HomeworkModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["teacher_id", "grade"]
