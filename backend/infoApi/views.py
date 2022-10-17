from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from AdminPanel.renderers import ErrorRenderer
from .serializers import (
    AdmissionInquirySerializer,
    AnnouncementSerializer,
    BlogsSerializer,
    CalendarEventSerializer,
    EventsSerializer,
    GallerySerializer,
    LeaveApplicationSerializer,
    NewsSerializer,
    RoutineExcleFileSerializer,
    RoutinesSerializer,
)
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

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 2000
    page_size_query_param = "page_size"


class AnnoucementAdminView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = AnnouncementSerializer
    queryset = AnnouncementModel.objects.all().order_by("date")
    pagination_class = CustomPagination


class AnnoucementPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = AnnouncementSerializer
    queryset = AnnouncementModel.objects.filter(status=True).order_by("-date")
    pagination_class = CustomPagination


class NewsAdminView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = NewsSerializer
    queryset = NewsModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(NewsModel, slug=item)


class NewsPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = NewsSerializer
    queryset = NewsModel.objects.filter(status=True).order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(NewsModel, slug=item)


class BlogsAdminView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = BlogsSerializer
    queryset = BlogModel.objects.all().order_by("-date")
    pagination_class = CustomPagination

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(BlogModel, slug=item)


class BlogsPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = BlogsSerializer
    queryset = BlogModel.objects.filter(status=True).order_by("-date")
    pagination_class = CustomPagination

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(BlogModel, slug=item)


class EventsAdminView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = EventsSerializer
    queryset = EventsModel.objects.all().order_by("-date")
    pagination_class = CustomPagination


class EventsPublicView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = EventsSerializer
    queryset = EventsModel.objects.filter(status=True).order_by("-date")
    pagination_class = CustomPagination


class CalendarEventView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = CalendarEventSerializer
    queryset = CalendarEventModel.objects.all().order_by("-start_date")


class CalendarEventApiView(APIView):
    renderer_classes = [ErrorRenderer]
    queryset = CalendarEventModel.objects.all()

    def post(self, request, format=None):
        getData = CalendarEventModel.objects.all()
        for data in getData:
            data.delete()
        serializer = CalendarEventSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoutineAdminView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = RoutinesSerializer
    queryset = RoutineModel.objects.all().order_by("date")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["grade", "exam_term"]


class RoutineExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = RoutineExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class LeaveApplicationView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = LeaveApplicationSerializer
    queryset = LeaveApplicationModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["stu_id"]


class AdmissionInquiryView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = AdmissionInquirySerializer
    queryset = AdmissionInquiryModel.objects.all().order_by("-date")
    pagination_class = CustomPagination


class GalleryView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = GallerySerializer
    queryset = GalleryModel.objects.all().order_by("-date")
    pagination_class = CustomPagination
