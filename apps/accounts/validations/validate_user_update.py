from rest_framework.exceptions import ValidationError



def validate_user_update(data):
    
    role_data = data.get('role_input')

    # maybe we use patch method which don't have the role_data data sent
    if role_data is None:
        return data

    if not Role.objects.filter(name=role_data).exists():
        raise ValidationError('The role you entered does not exist!') 

    return data
    
