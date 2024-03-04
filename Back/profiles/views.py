from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
import os

from .models import Profile, Favorite
from .serializers import SerializeSimpleProfile, SerializeProfile


class ProfilesClassView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializeSimpleProfile
    queryset = Profile.objects.filter(active=True)

    def list(self, request, *args):
        """
            Função que busca a lista com o perfil de todos os profissionais
        """
        query = self.get_queryset()
        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
            Função que retorna o perfil detalhado de um usuario especifico
            !!! post foi usado para permitir passar o id via form !!!

            Parameters:
                - id: id do perfil, se o valor for None retorna o perfil do usuario
        """
        try:
            your_id = request.user.profile.id or None
            profile_id = request.data.get("profileId", your_id)
            query = get_object_or_404(Profile, pk=profile_id, active=True)  # se não encontrado retorna 404
            serializer = SerializeProfile(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, ValueError, TypeError):
            return Response({"error": "Perfil não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ Impede que delete o perfil """
        pass


class YourProfileClassView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializeProfile
    queryset = []

    def create(self, request, *args, **kwargs):
        """
            Cria ou atualiza o perfil do usuario
        """
        try:

            user = request.user
            picture = request.data.get('image', None)
            name = request.data['name']
            lastname = request.data['lastName']
            area = request.data['area']
            profession = request.data['profession']
            email = request.user.email
            telephone = request.data['telephone']
            description = request.data['description']
            active = request.data['active']

            profile, created = Profile.objects.get_or_create(user=user)
            profile.name = name
            profile.lastname = lastname
            profile.area = area
            profile.profession = profession
            profile.email = email
            profile.telephone = telephone
            profile.description = description
            profile.active = str(active).title()

            if picture and profile.picture:
                file_path = f"media/{profile.picture}"
                if os.path.exists(file_path):
                    os.remove(file_path)
                profile.picture = picture
            profile.save()
            serializer = self.get_serializer(profile, many=False)
            return Response(serializer.data, status=200)
        except (KeyError, ValueError, TypeError):
            return Response({"error": "Não foi possivel localizar o perfil"}, status=500)

    def destroy(self, request, *args, **kwargs):
        """ Impede que o perfil seja deletado """
        pass


# Favorites
class FavoriteClassView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializeSimpleProfile
    queryset = []

    def create(self, request, *args, **kwargs):
        """
            Adicona ou remove um professinal aos favoritos do usuario
        """
        try:
            profile_id = request.data['profileId']
            user = request.user
            professional = Profile.objects.get(pk=profile_id)
            professional_name = f"{professional.profession} {professional.name}"
            favorite, created = Favorite.objects.get_or_create(user=user, professional=professional)
            if created:
                return Response({"msg": f"{professional_name} adiconado aos favoritos"}, status=200)
            else:
                favorite.delete()
                return Response({"msg": f"{professional_name} removido dos favoritos"}, status=200)
        except (KeyError, ValueError, ObjectDoesNotExist):
            return Response({"error": "Não foi possivel adicionar aos favoritos"}, status=400)

    def destroy(self, request, *args, **kwargs):
        """ Impede que delete o favorito """
        pass
