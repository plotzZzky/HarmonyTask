from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    question = SerializerMethodField()
    answer = SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'question', 'answer']

    @staticmethod
    def get_question(obj):
        return obj.recovery.question

    @staticmethod
    def get_answer(obj):
        return obj.recovery.answer
