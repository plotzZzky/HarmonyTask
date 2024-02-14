from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import mixins, status
from django.core.exceptions import ObjectDoesNotExist
import os

from .models import Profile, Favorite
from .serializers import SerializeSimpleProfile, SerializeProfile


class ProfilesClassView(GenericAPIView):
    IsAuthenticated = True

    def get(self, request):
        """
            Função que busca a lista com o perfil de todos os profissionais
        """
        query = Profile.objects.filter(active=True)
        serializer = SerializeSimpleProfile(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
            Função que retorna o perfil detalhado de um usuario especifico
        """
        try:
            profile_id = request.data.get("profileId")
            query = get_object_or_404(Profile, pk=profile_id, active=True)
            serializer = SerializeProfile(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "Perfil não encontrado"}, status=status.HTTP_400_BAD_REQUEST)


class YourProfileClassView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericAPIView):
    IsAuthenticated = True

    def get(self, request):
        profile = request.user.profile
        serializer = SerializeProfile(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
            Função que retorna o perfil detalhado de um usuario especifico
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

            # Tenta obter o perfil existente ou cria um novo se não existir
            profile, created = Profile.objects.get_or_create(user=user)
            if not created:
                # Se o perfil já existir, atualiza os dados
                profile.name = name
                profile.lastname = lastname
                profile.area = area
                profile.profession = profession
                profile.email = email
                profile.telephone = telephone
                profile.description = description
                profile.active = bool(active)
                if picture:
                    os.remove(f"media/{profile.picture}")
                    profile.picture = picture
            else:
                profile = Profile.objects.create(
                    user=user, name=name, lastname=lastname, area=area, profession=profession, email=email,
                    telephone=telephone, description=description, picture=picture, active=True
                )
            profile.save()
            return Response({"msg": "Perfil criado"}, status=200)
        except (KeyError, ValueError):
            return Response({"error": "Não foi possivel localizar o perfil"}, status=500)


# Favorites
class FavoriteClassView(GenericAPIView):
    IsAuthenticated = True

    def get(self, request):
        favorites = request.user.favorites.all()
        serializer = SerializeSimpleProfile(favorites)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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
            return Response({"error": "Não foi possivel adicionar aos favoritos"}, status=500)
