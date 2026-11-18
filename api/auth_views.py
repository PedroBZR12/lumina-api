from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core import signing
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from urllib.parse import urlencode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.authentication import TOKEN_SALT, issue_token
from api.models import CareGiver


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        caregiver = (
            CareGiver.objects.filter(email__iexact=email).first()
            if isinstance(email, str)
            else None
        )
        if (
            caregiver is None
            or not isinstance(password, str)
            or not check_password(password, caregiver.password)
        ):
            return Response(
                {"detail": "E-mail ou senha inválidos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response({"token": issue_token(caregiver)})


class PasswordResetRequestView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        caregiver = (
            CareGiver.objects.filter(email__iexact=email).first()
            if isinstance(email, str)
            else None
        )
        if caregiver:
            token = signing.dumps(
                {
                    "caregiver_id": caregiver.pk,
                    "password": caregiver.password,
                },
                salt=f"{TOKEN_SALT}.password-reset",
            )
            separator = "&" if "?" in settings.PASSWORD_RESET_URL else "?"
            reset_url = (
                f"{settings.PASSWORD_RESET_URL}{separator}"
                f"{urlencode({'email': caregiver.email, 'token': token})}"
            )
            send_mail(
                "Redefinição de senha - Lumina",
                f"Use este link para redefinir sua senha: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [caregiver.email],
            )
        return Response(
            {"detail": "Se o e-mail estiver cadastrado, enviaremos as instruções."}
        )


class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        token = request.data.get("token", "")
        password = request.data.get("password", "")
        if not all(isinstance(value, str) for value in (email, token, password)):
            return Response(
                {"detail": "E-mail, token e senha devem ser texto."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(password) < 8:
            return Response(
                {"password": "A senha deve ter ao menos 8 caracteres."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            payload = signing.loads(
                token,
                salt=f"{TOKEN_SALT}.password-reset",
                max_age=60 * 60,
            )
        except signing.BadSignature:
            return Response(
                {"token": "Token inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        caregiver = get_object_or_404(
            CareGiver,
            pk=payload.get("caregiver_id"),
            email__iexact=email,
        )
        if payload.get("password") != caregiver.password:
            return Response(
                {"token": "Token inválido ou já utilizado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        caregiver.password = make_password(password)
        caregiver.save(update_fields=("password",))
        return Response({"detail": "Senha alterada com sucesso."})
