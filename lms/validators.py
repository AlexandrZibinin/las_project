from rest_framework.serializers import ValidationError
from urllib.parse import urlparse

allowed_resurce = ['youtube.com']


def validate_resurce(value):
    """проверка разрешенного ресурса из поля видео"""
    domain = urlparse(value).netloc
    val_domain = ('.'.join(domain.split('.')[-2:]))
    if val_domain not in allowed_resurce:
        raise ValidationError('Недопустимый ресурс')
