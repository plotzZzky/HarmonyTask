from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Recovery


class SerializerUser(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class SerializerRecovery(ModelSerializer):
    class Meta:
        model = Recovery
        fields = '__all__'
