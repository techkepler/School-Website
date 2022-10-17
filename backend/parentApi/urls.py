from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parentApi import views

app_name = "parentApi"

router = DefaultRouter()

router.register(
    "parent", views.CRUDParentViewAdmin, basename="parent_crud_operation_admin"
)

router.register(
    "parents/public",
    views.CRUDParentViewPublic,
    basename="parent_crud_operation_public",
)

urlpatterns = [
    path("crud/", include(router.urls)),
    path(
        "register/excel/file/",
        views.ParentRegisterExcelView.as_view(),
        name="parent_register_excel",
    ),
]
