from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
import jwt
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.middleware import csrf
from django.http import JsonResponse

from AdminPanel.renderers import ErrorRenderer
from .models import User
from teacherApi.models import TeacherDataCollection
from staffApi.models import StaffDataCollection
from studentApi.models import StudentDataCollection
from parentApi.models import ParentDataCollection

from .serializers import (
    CookieTokenRefreshSerializer,
    CreateUserSerializer,
    DeleteUserSerializer,
    PasswordResetSerializer,
    UserLoginSerializer,
    UserPasswordChangeSeriaizer,
    UserSerializer,
)

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 5000
    page_size_query_param = "page_size"


# function to create custom jwt token for user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# get Csrf
def get_csrf(request):
    response = JsonResponse({"Info": "Success - Set CSRF cookie"})
    response["X-CSRFToken"] = csrf.get_token(request)
    return response


class PublicUserView(ModelViewSet):
    renderer_classes = [ErrorRenderer]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("uid")
    pagination_class = CustomPagination


class CreateUserView(APIView):
    renderer_classes = [ErrorRenderer]
    queryset = User.objects.all()

    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login
class UserLoginApiView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        response = Response()
        if serializer.is_valid(raise_exception=True):
            uid = serializer.data.get("uid")
            password = serializer.data.get("password")
            get_user = User.objects.filter(uid=uid)
            
            if not get_user.exists():
                return Response(
                    {"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
            else:
                grab_user = User.objects.get(uid=uid)
                user = authenticate(uid=uid, password=password)
                if user:
                    token = get_tokens_for_user(user)
                    user_code = [454545]
                    if grab_user.role == "Student":
                        stu = StudentDataCollection.objects.get(id=uid)
                        user_code.append(2481237951)

                        msg = "Logged In Successfully."
                        response.set_cookie(
                            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                            value=token["refresh"],
                            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                        )
                        response.data = {
                            "msg": msg,
                            "token": token.get("access"),
                            "role": user_code,
                            "category": "Student",
                            "name": stu.name,
                            "uid": uid,
                            "grade":stu.grade,
                            "email":stu.email
                        }
                        return response
                    
                    elif grab_user.role == "Teacher":
                        teacher = TeacherDataCollection.objects.get(id=uid)
                        user_code.append(5379482180)
                        msg = "Logged In Successfully."
                        response.set_cookie(
                            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                            value=token["refresh"],
                            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                        )
                        response.data = {
                            "msg": msg,
                            "token": token.get("access"),
                            "role": user_code,
                            "category": "Teacher",
                            "name": teacher.name,
                            "uid": uid,
                            "email":teacher.email
                        }
                        return response

                    elif grab_user.is_admin == True:
                        user_code.append(2846728426)
                        msg = "Logged In Successfully."
                        response.set_cookie(
                            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                            value=token["refresh"],
                            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                        )
                        response.data = {
                            "msg": msg,
                            "token": token.get("access"),
                            "role": user_code,
                            "category": "Admin",
                            "name": "Bishal Rayamajhi",
                            "uid": uid,
                            "email":"rayamajhibishal289@gmail.com"
                        }
                        return response
                                    
                    else:
                        msg = "You are not allowed to login."
                        return Response({"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    msg = "Invalid Credentials"
                    return Response({"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# password change
class PasswordChangeView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = UserPasswordChangeSeriaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete User


class DeleteUserView(APIView):
    renderer_classes = [ErrorRenderer]

    def post(self, request, format=None):
        serializer = DeleteUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        return super().finalize_response(request, response, *args, **kwargs)



class UserInformationApiView(APIView):
    
    def get(self, request, format=None):
        # response = Response()
        get_cookie = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) or None
        data = jwt.decode(jwt=get_cookie, key=settings.SECRET_KEY, algorithms=["HS256"])
        print("datas", data)
        usr_id = data.get("user_id")
        print("usr_id........", usr_id)
        is_user = User.objects.filter(id=usr_id)
        user_code = [454545]
        if is_user.exists():
            get_user = User.objects.get(id=usr_id)
            if get_user.is_admin == True:
                user_code.append(2846728426)
                return Response(
                    {
                        "role": user_code,
                        "name": "Bishal Rayamajhi",
                        "category": get_user.role,
                        "uid": get_user.uid,
                        "email":"rayamajhibishal289@gmail.com"
                    },
                    status=status.HTTP_200_OK,
                )
            elif get_user.is_staff == True:
                user_code.append(5379482180)
                teacher = TeacherDataCollection.objects.get(id=get_user.uid)
                return Response(
                    {
                        "role": user_code,
                        "name": teacher.name,
                        "category": get_user.role,
                        "uid": get_user.uid,
                        "email":teacher.email
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                user_code.append(2481237951)
                stu = StudentDataCollection.objects.get(id=get_user.uid)
                print("students....", stu)
                return Response(
                    {
                        "role": user_code,
                        "name": stu.name,
                        "category": get_user.role,
                        "uid": get_user.uid,
                        "grade":stu.grade,
                        "email":stu.email
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"msg": "User doesn't exists."}, status=status.HTTP_400_BAD_REQUEST
            )
