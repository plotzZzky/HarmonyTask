from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Profile, Favorite


class SerializeSimpleProfile(ModelSerializer):
    """
        Retorna apenas os campos basicos, para criar a lista com todos os perfis de profissionais no front
    """

    favorite = SerializerMethodField()

    def get_favorite(self, obj):
        try:
            Favorite.objects.get(professional=obj)
            result = True
        except Favorite.DoesNotExist:  # type:ignore
            result = False
        return result

    class Meta:
        model = Profile
        fields = ['id', 'name', 'lastname', 'area', 'profession', 'picture', 'favorite']


class SerializeProfile(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
