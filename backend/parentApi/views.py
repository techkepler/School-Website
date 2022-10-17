from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from AdminPanel.renderers import ErrorRenderer
from .serializers import ParentCRUDSerializer, ParentRegisterExcleFileSerializer
from .models import ParentDataCollection

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 40


class CRUDParentViewAdmin(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = ParentCRUDSerializer
    queryset = ParentDataCollection.objects.all().order_by("name")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id"]


class CRUDParentViewPublic(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = ParentCRUDSerializer
    queryset = ParentDataCollection.objects.all().order_by("name")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "id"]


class ParentRegisterExcelView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = ParentRegisterExcleFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
