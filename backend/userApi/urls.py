from django.urls import path, include
from rest_framework.routers import DefaultRouter
from userApi import views

app_name = "userApi"

router = DefaultRouter()

router.register(
    "public",
    views.PublicUserView,
    basename="public_user_crud_operation_admin",
)


urlpatterns = [
    path("crud/", include(router.urls)),
    path("csrf/", views.get_csrf, name="csrf_check"),
    path("create/", views.CreateUserView.as_view(), name="create_user"),
    path("login/", views.UserLoginApiView.as_view(), name="login_user"),
    path(
        "password/change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path("password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("delete/user/", views.DeleteUserView.as_view(), name="delete_user"),
    path(
        "refresh/token/", views.CookieTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("information/", views.UserInformationApiView.as_view(), name="user_info"),
]
