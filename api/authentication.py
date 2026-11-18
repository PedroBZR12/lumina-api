from django.core import signing
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api.models import CareGiver

TOKEN_SALT = "api.caregiver-token"
TOKEN_MAX_AGE = 60 * 60 * 8


def issue_token(caregiver):
    return signing.dumps(
        {
            "caregiver_id": caregiver.pk,
            "password": caregiver.password,
            "issued_at": timezone.now().isoformat(),
        },
        salt=TOKEN_SALT,
    )


class CaregiverTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get("Authorization", "")
        if not authorization:
            return None

        scheme, separator, token = authorization.partition(" ")
        if not separator or scheme.lower() != "token" or not token:
            raise AuthenticationFailed("Use Authorization: Token <token>.")

        try:
            payload = signing.loads(
                token,
                salt=TOKEN_SALT,
                max_age=TOKEN_MAX_AGE,
            )
            caregiver = CareGiver.objects.get(pk=payload["caregiver_id"])
            if payload["password"] != caregiver.password:
                raise AuthenticationFailed("Token invalidado.")
        except (signing.BadSignature, KeyError, CareGiver.DoesNotExist) as exc:
            raise AuthenticationFailed("Token inválido ou expirado.") from exc

        return caregiver, token

    def authenticate_header(self, request):
        return "Token"
