from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

def validate_noHp(value):
    for word in value:
        if not bool(re.search('\d', word)):
            message = 'Maaf nilai mengandung angka'
            raise ValidationError(message)

def validate_noHp_exist(value):
    try:
        User.objects.get(username=value)
    except User.DoesNotExist:
        return value
    raise ValidationError('No hp telah terdaftar')

def validate_noHp_not_exist(value):
    try:
        User.objects.get(username=value)
    except User.DoesNotExist:
        return value
    raise ValidationError('No hp telah terdaftar')
