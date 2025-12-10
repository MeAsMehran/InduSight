from rest_framework import serializers
from .models import CustomUser, Role
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']


from apps.accounts.validations.validate_user_register import validate_register
class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, validators=[validate_password])

    role = RoleSerializer(read_only=True)
    role_input = serializers.ChoiceField(choices=Role.ROLE_CHOICES, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'name', 'password', 'confirm_password', 'role', 'role_input')

    def validate(self, data):
        return validate_register(data)

    def create(self, validated_data):
        role_name = validated_data.pop('role_input')
        role = Role.objects.get(name=role_name)

        password = validated_data.pop("password")
        validated_data.pop("confirm_password")

        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        user.role = role
        user.save()
        return user



from apps.accounts.validations.validate_user_login import validate_login
class CustomUserLoginSerializer(serializers.Serializer):
    """
        For Serializing the User Login
    """
    phone_number = PhoneNumberField(region="IR")
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.DictField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['phone_number']
        
    def validate(self, data):
        return validate_login(data)


class CustomUserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'phone_number', 'email')






