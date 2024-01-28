from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


def create_new_token(user):
    """
        Função que retona um novo token para o usuario
        Essa função cria um novo token a cada login, para evitar problemas com vazamento de token

        Steps:
            - Verifica se o usuario ja possui token
                - Passes:
                    - Deleta o token antigo
                - Fails:
                    - Continua a execução
            - Cria um novo token para o usuario

        Parameters:
            - user (User): A referencia do Objeto do usuario

        Return:
            O novo token
    """
    try:
        token = Token.objects.get(user=user)  # type: ignore
        token.delete()
    except ObjectDoesNotExist:
        pass

    new_token = Token.objects.create(user=user)  # type: ignore
    new_token.save()
    return new_token
