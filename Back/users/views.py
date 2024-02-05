from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError

from .validate import validate_user, validate_password
from .token import create_new_token
from .models import Recovery
from .serializer import SerializerRecovery, SerializerUser
from .update import update_profile

from profiles.serializers import SerializeProfile


@api_view(['POST'])
def register_user(request):
    """
        Função para registar um novo usuario

        Steps:
            - Recebe os valores via form
            - Verifica se os valores são validos:
                - Passes:
                    - Tenta autenticar o usuario e cria um token:
                    - Retorna um JSON com a mensagem de sucesso e o token
                - Fails:
                    - Retorna um Json com a mensagem de erro

        Parameters:
            - password (str) : Senha do usuario
            - pwd (str) : Senha para confirmação
            - email (email) : Email do usaurio

        Return:
            Se a criação do usuario der certo, retorna um json com o token, se não, retorna uma resposta com o erro

    """
    try:
        password = request.data['password']
        pwd = request.data['pwd']
        username = request.data['username']
        email = request.data['email']

        question = request.data['question']
        answer = request.data['answer']
        hashed_answer = make_password(answer)

        user_valid = validate_user(password, pwd, username, email)

        if user_valid:
            user = User(username=username, email=email, password=password)
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            Recovery.objects.create(user=user, question=question, answer=hashed_answer)

            token = create_new_token(user)  # Função que cria um novo token
            return Response({"token": token.key}, status=200)
        else:
            return Response({"error": user_valid}, status=401)
    except (AttributeError, KeyError):
        return Response({"error": "Preencha os campos corretamente para cadastrar!"}, status=500)
    except IntegrityError as error:
        if 'auth_user_username_key' in str(error):
            field = 'Nome de usuario'
        else:
            field = 'O e-mail'
        return Response({"error": f"{field} já existe e não pode ser cadastrado!"}, status=500)


class LoginView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        """
            Função de login do usuario.

            Steps:
                - Recebe os valores via form
                - Tenta a autenticação
                    - Passes:
                        - Retorna um JSON com a resposta de sucesso e o token
                    - Fails:
                        - Retorna um Json com a resposta de erro
            Parameters:
                - password (str): Senha do usuario
                - username (str): Nome do usuario

            Return:
                Se a autenticação der certo retorna um json com o token, do contário, retorna uma mensagem de erro

        """
        try:
            password = request.data['password']
            username = request.data['username']

            user = authenticate(username=username, password=password)
            if user:
                token = create_new_token(user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Login incorreto!"}, status=status.HTTP_401_UNAUTHORIZED)
        except (KeyError, ValueError):
            return Response({"error": "Login incorreto"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    """
        Função que retorna as informações do usario para precher a pagina de atualização do usuario no front
    """
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None

    user_data = SerializerUser(user).data
    recovery_data = SerializerRecovery(user.recovery).data
    profile_data = SerializeProfile(profile).data if profile else {}

    data = {**user_data, **recovery_data, **profile_data}

    return Response({"user": data}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_your_profile(request):
    """
        Função para atualizar o perfil profissional

        Steps:
            - Recebe os valores via form
            - Valida os dados
                - Passes:
                    - Atualiza os dados
                - Fails:
                    - Ignora e segue para o proximo

        Parameters:
            - name (str): Nome do usuario
            - lastname (str): Sobrenome do usuario
            - area (str): Area de atuação do profissional
            - profession (str): Profissão do usaurio
            - telephone (str): Telefone do usuario
            - description (str): Descrição do perfil do profissional
            - active (bol): Perfil ativo ou não

        Return:
            - Retorna um JSON com uma mensagem de status
    """
    try:
        profile = request.user.profile
        name = request.data.get('name', None)
        lastname = request.data.get('lastname', None)
        area = request.data.get('area', None)
        profession = request.data.get('profession', None)
        telephone = request.data.get('telephone', None)
        description = request.data.get('description', None)
        active = request.data.get('active', None)

        update_profile(profile, name, lastname, area, profession, telephone, description, active)
        return Response({"msg": "Perfil atualizado!"}, status=200)

    except (KeyError, ValueError):
        return Response({"error": "Não foi possivel atualizar o perfil!"}, status=500)


@api_view(['POST'])
def recovery_password(request):
    """
        Função para recuperação da senha atraves do resposta da pergunta de recuparação de senha
        
        Steps:
            - Recebe os valores
            - Verifica se a resposta está correta
                - Passes:
                    - Valida a senha e atualiza ela
                    - Retorna um JSON coma e mensagem de sucesso
                - Fails:
                    - Retorna um JSON com a mensagem de errro

        Parameters:
            - username (str): Nome do usuario
            - passwrod (sr): Senha do usuario
            - pwd (str): Confirmação de senha
            - answer (str): Resposta para a recuperação da senha
    """
    try:
        username = request.data['username']
        answer = request.data['answer']
        password = request.data['password']
        pwd = request.data['pwd']
        user = User.objects.get(username=username)
        if check_password(answer, user.profile.answer):
            if validate_password(password, pwd):
                user.set_password(password)
                user.save()
                return Response({"msg": "Senha atualizada!"}, status=200)
            else:
                return Response(
                    {"msg": "As senhas precisam ser iguais, no minimo uma letra, numero e 8 digitos!"}, status=500)
        else:
            raise ValueError()
    except (KeyError, ValueError, ObjectDoesNotExist):
        return Response({"msg": "Resposta incorreta!"}, status=500)
    

# Envia a question do usuario para o front para fazer a recuperação de senha
class ReceiverYourQuestion(GenericAPIView):
    def post(self, request, *args, **kwargs):
        """
            Função que retorna a pergunta de recuperação de senha para o front, usada para a tela de recuperação de senha
            do usuario

            Steps:
                - Recebe os valores
                - Procura o usuario
                    - Passes:
                        - Retorna um JSON uma mensagem de sucesso
                    - Fails:
                        - Retorna uma mensagem de erro
        """
        try:
            username = request.data['username']
            user = User.objects.get(username=username)
            question = user.profile.question
            return Response({"question": question}, status=status.HTTP_200_OK)
        except (KeyError, ValueError, ObjectDoesNotExist):
            return Response({"error": "Usuario não encontrado"}, status=status.HTTP_400_BAD_REQUEST)