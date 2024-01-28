from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from .models import Profile, Favorite
from .serializers import SerializeSimpleProfile, SerializeProfile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_professionals(request):
    """
        Função que busca a lista com o perfil de todos os profissionais

        Parameters:
            - area (str) default="": A area de atuação do profissional

        Return:
            - JSON com a lista de perfis
    """
    area = request.data.get('area', None)
    if area:
        query = Profile.objects.all().filter(area=area, active=True)
    else:
        query = Profile.objects.all().filter(active=True)
    data = SerializeSimpleProfile(query, many=True).data
    return Response({"profiles": data}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_professional_profile(request):
    """
        Função que retorna o perfil detalhado de um usuario especifico
    """
    try:
        profile_id = request.data.get('profileId', request.user.profile.id)
        query = Profile.objects.get(pk=profile_id)
        data = SerializeProfile(query).data
        return Response({"profile": data}, status=200)
    except (KeyError, ValueError):
        return Response({"error": "Não foi possivel localizar o perfil"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_your_profile(request):
    """
        Função que retorna o perfil detalhado de um usuario especifico
    """
    try:
        profile_id = request.user.profile.id
        query = Profile.objects.get(pk=profile_id)
        data = SerializeProfile(query).data
        return Response({"profile": data}, status=200)
    except (KeyError, ValueError, ObjectDoesNotExist):
        return Response({"error": "Não foi possivel localizar o perfil"}, status=500)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def update_your_profile(request):
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
        profile, created = Profile.objects.get_or_create(
            user=user, name=name, lastname=lastname, area=area, profession=profession, email=email,
            telephone=telephone, description=description, picture=picture
        )

        if not created:
            # Se o perfil já existir, atualiza os dados
            profile.name = name
            profile.lastname = lastname
            profile.area = area
            profile.profession = profession
            profile.email = email
            profile.telephone = telephone
            profile.description = description
            profile.active = active
            if picture:
                profile.picture = picture
            profile.save()
        return Response({"msg": "Perfil criado"}, status=200)
    except (KeyError, ValueError):
        return Response({"error": "Não foi possivel localizar o perfil"}, status=500)


# Favorites
@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def add_professional_favorites(request):
    """
        Adicona ou remove um professinal aos favoritos do usuario
    """
    try:
        professional_id = request.data['professionalId']
        user = request.user
        professional = Profile.objects.get(pk=professional_id)
        professional_name = f"{professional.profission} {professional.name}"
        favorite, created = Favorite.objects.get_or_create(user=user, professional=professional)
        if created:
            return Response({"msg": f"{professional_name} adiconado aos favoritos"}, status=200)
        else:
            favorite.delete()
            return Response({"msg": f"{professional_name} removido dos favoritos"}, status=200)
    except (KeyError, ValueError, ObjectDoesNotExist):
        return Response({"error": "Não foi possivel adicionar aos favoritos"}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_your_favorites(request):
    """
        Recebe a lista com os favoritos do usuario
    """
    user = request.user
    favorites = user.favorites.all()
    data = SerializeSimpleProfile(favorites).data
    return Response({"favorites": data}, status=200)
