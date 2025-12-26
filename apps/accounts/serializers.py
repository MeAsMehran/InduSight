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


# This is for admin crate a user
from apps.accounts.validations.validate_user_register import validate_user_creation
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_input = serializers.ChoiceField(choices=Role.ROLE_CHOICES, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number', 'name', 'email', 'role', 'role_input')

    
from apps.accounts.validations.validate_user_update import validate_user_update
class UserUpdateSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)   # read_only only appears in the Response 
    role_input = serializers.ChoiceField(choices=Role.ROLE_CHOICES, write_only=True, required=False)    # write_only is only for entering the data
    
    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'role', 'role_input')

    def validate(self, attrs):
        return validate_user_update(attrs)

    def update(self, instance, validated_data):
        name = validated_data.pop('name', instance.name)
        email = validated_data.pop('email', instance.email)
        role_input = validated_data.pop('role_input', instance.role)

        # role should be instance to assign it to the instance and update the role of the user
        role = Role.objects.get(name=role_input)

        instance.name = name
        instance.email = email
        instance.role = role

        instance.save()
        return instance

        




