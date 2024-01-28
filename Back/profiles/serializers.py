from rest_framework.serializers import ModelSerializer

from .models import Profile


class SerializeSimpleProfile(ModelSerializer):
    """
        Retorna apenas os campos basicos, para criar a lista com todos os perfis de profissionais no front
    """
    class Meta:
        model = Profile
        fields = ['id', 'name', 'lastname', 'area', 'profession', 'picture']


class SerializeProfile(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
