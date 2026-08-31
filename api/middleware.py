from decouple import config
from django.http import JsonResponse
from django.core.cache import cache

PUBLIC_ROUTES = [
    "/api/login/",
    "/api/register/",
]


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        cache_key = f"rate_limit_{ip}"
        requests_count = cache.get(cache_key, 0)

        if requests_count >= 15:
            return JsonResponse(
                {"erro": "Muitas requisições. Tente novamente mais tarde."},
                status=429
            )

        cache.set(cache_key, requests_count + 1, timeout=300)

        if request.path not in PUBLIC_ROUTES:
            if not request.user.is_authenticated:
                return JsonResponse(
                    {"erro": "Autenticação necessária."},
                    status=401
                )
            if "api/admin/" in request.path and not request.user.is_staff:
                return JsonResponse(
                    {"erro": "Acesso negado."},
                    status=403
                )

        response = self.get_response(request)

        # CORS        
        response["Access-Control-Allow-Origin"] = config("ALLOWED_ORIGIN")
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        # Segurança
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        
        return response 