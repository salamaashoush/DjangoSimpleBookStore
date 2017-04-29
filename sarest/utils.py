from rest_framework import serializers

from sarest.serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': 'JWT '+token,
        'user': UserSerializer(user, context={'request': request}).data
    }
