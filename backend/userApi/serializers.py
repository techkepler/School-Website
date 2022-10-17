from operator import truediv
from rest_framework import serializers
from django.forms import ValidationError
from .models import User
from teacherApi.models import TeacherDataCollection
from staffApi.models import StaffDataCollection
from studentApi.models import StudentDataCollection
from parentApi.models import ParentDataCollection

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["uid", "role", "is_active", "is_admin", "is_staff"]
        model = User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["uid", "role", "password"]
        model = User

    def validate(self, attrs):
        uid = attrs.get("uid")
        role = attrs.get("role")

        if role == "Student":
            if not StudentDataCollection.objects.filter(id=uid).exists():
                raise ValidationError("Given User Id didn't match with any Student Id.")

        elif role == "Teacher":
            if not TeacherDataCollection.objects.filter(id=uid).exists():
                raise ValidationError("Given User Id didn't match with any Teacher Id.")

        elif role == "Staff":
            if not StaffDataCollection.objects.filter(id=uid).exists():
                raise ValidationError("Given User Id didn't match with any Staff Id.")

        elif role == "Parent":
            if not ParentDataCollection.objects.filter(id=uid).exists():
                raise ValidationError("Given User Id didn't match with any Parent Id.")

        return attrs

    def create(self, validated_data):
        get_role = validated_data.get("role")
        get_uid = validated_data.get("uid")
        get_password = validated_data.get('password')
        is_staff = False
        
        if get_role == "Teacher":
            is_staff = True
        return User.objects.create_user(
            uid = get_uid, role = get_role, is_staff = is_staff, password=get_password
        )


# creating a UserLogin serializer
class UserLoginSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ["uid", "password"]


# Creating PasswordChange Serializer
class UserPasswordChangeSeriaizer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    old_password = serializers.CharField(
        label="password", style={"input_type": "password"}, write_only=True
    )
    password = serializers.CharField(
        label="password", style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        label="confirm password", style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["uid", "password", "confirm_password", "old_password"]

    def validate(self, attrs):
        uid = attrs.get("uid")
        print(uid)
        password = attrs.get("password")
        confrim_password = attrs.get("confirm_password")
        old_password = attrs.get("old_password")
        user = User.objects.get(uid=uid)

        if password != confrim_password:
            raise ValidationError("Password and Confrim Password doesn't matches.")
        elif not user.check_password(old_password):
            raise ValidationError("Invalid Old Password")

        return attrs

    def create(self, validated_data):
        user = User.objects.get(uid=validated_data.get("uid"))
        user.set_password(validated_data.get("password"))
        user.save()
        return validated_data


class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    password = serializers.CharField(
        label="password", style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        label="confirm password", style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["uid", "password", "confirm_password"]

    def validate(self, attrs):
        uid = attrs.get("uid")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if not User.objects.filter(uid=uid).exists():
            raise ValidationError("Given User ID doesn't exist.")
        elif password != confirm_password:
            raise ValidationError("Password and Confirm Password did not match.")

        return super().validate(attrs)

    def create(self, validated_data):
        uid = validated_data.get("uid")
        password = validated_data.get("password")
        get_user = User.objects.get(uid=uid)
        get_user.set_password(password)
        get_user.save()
        return validated_data


class DeleteUserSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)

    class Meta:
        fields = ["uid"]

    def validate(self, attrs):
        get_id = attrs.get("uid")
        if not User.objects.filter(uid=get_id).exists():
            raise ValidationError("Given User Id doesn't exist.")
        else:
            get_user = User.objects.get(uid=get_id)
            if get_user.is_superuser == True:
                raise ValidationError("You are not authorized to delete this user.")
            elif get_user.is_admin == True:
                raise ValidationError("You are not authorized to delete this user.")

        return super().validate(attrs)

    def create(self, validated_data):
        get_user = get_user = User.objects.get(uid=validated_data.get("uid"))
        get_user.delete()
        return validated_data



class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh_token'")