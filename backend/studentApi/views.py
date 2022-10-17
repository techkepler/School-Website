from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from AdminPanel.renderers import ErrorRenderer
from studentApi.serializers import (
    AttendanceResetSerializer,
    FeeResetSerializer,
    StudentAbsentSerializer,
    StudentAttendanceExcleFileSerializer,
    StudentAttendanceSerializer,
    StudentCRUDSerializer,
    StudentFeeExcleFileSerializer,
    StudentFeePaymentSerializer,
    StudentFeeSerializer,
    StudentGradeUpdateSerializer,
    StudentRegisterExcleFileSerializer,
    StudentResutlSerializer,
    UpdateAbsentSerializer,
    UpdateAttendanceSerializer,
    UpdateFeeSerializer,
)
from studentApi.models import (
    StudentAbsentModel,
    StudentAttendanceModel,
    StudentDataCollection,
    StudentFeeModel,
    StudentResultCollectionModel,
)

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 40


# Student CRUD VIEWS


class CRUDStudentViewAdmin(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentCRUDSerializer
    queryset = StudentDataCollection.objects.all().order_by("name")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id"]


class CRUDStudentViewPublic(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentCRUDSerializer
    queryset = StudentDataCollection.objects.all().order_by("name")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id", "grade"]


class StudentRegisterExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StudentRegisterExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StudentClassUpdateView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StudentGradeUpdateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ...................Student Attendance Views..........................


class StudentAttendanceCRUDPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentAttendanceSerializer
    queryset = StudentAttendanceModel.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name", "grade"]


class StudentAttendanceRegisterView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentAttendanceSerializer
    queryset = StudentAttendanceModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class StudentAttendanceRegisterExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StudentAttendanceExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StudentUpdateAttendanceView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateAttendanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StudentAbsentUpdateView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateAbsentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class ResetStudentAttendanceView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = AttendanceResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors)


class StudenAbsentView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentAbsentSerializer
    queryset = StudentAbsentModel.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student_details", "name"]


# ........... Student Fee View ..............


class StudentFeeCRUDPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentFeeSerializer
    queryset = StudentFeeModel.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name", "grade"]


class StudentFeeView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentFeeSerializer
    queryset = StudentFeeModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


class StudentFeeExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StudentFeeExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StudentUpdateFeeView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UpdateFeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StudentFeePaymentView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StudentFeePaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StudentFeePaymentStoreView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = StudentFeePaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class ResetStudentFeeView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = FeeResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors)


# Student Result View


class StudentResultCRUDPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentResutlSerializer
    queryset = StudentResultCollectionModel.objects.all().order_by("subject")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["stu_details", "name", "exam_term", "grade"]


class StudentResultCRUDAdminView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = StudentResutlSerializer
    queryset = StudentResultCollectionModel.objects.all().order_by("stu_details")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["stu_details", "name", "exam_term", "grade"]


class DeletStuResultView(APIView):
    renderer_classes = [ErrorRenderer]

    def delete(self, request, format=None):
        get_result = StudentResultCollectionModel.objects.all()
        for result in get_result:
            result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
