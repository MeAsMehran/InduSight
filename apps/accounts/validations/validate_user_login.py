from rest_framework.exceptions import AuthenticationFailed
from apps.accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


def validate_login(data):
    """
        make phone number to start with 0...

        raise errors:
            - User not fount
            - Invalid password

        return:
            - phone_number
            - refresh
            - access
    """

    phone_number_value = str(data['phone_number']).replace('+98', '0')
    password_value = data['password']

    user = CustomUser.objects.filter(phone_number=phone_number_value).first()

    if not user:
        raise AuthenticationFailed('User not found or invalid password')
    
    if not user.check_password(password_value):
        raise AuthenticationFailed('User not found or invalid password!')
    
    refresh = RefreshToken.for_user(user)

    return {
        'phone_number': phone_number_value,
        'token' : {
            'refresh' : str(refresh),
            'access' : 'Bearer ' + str(refresh.access_token),
        }
    }
