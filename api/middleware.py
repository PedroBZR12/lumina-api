from decouple import config
from django.http import JsonResponse
from django.core.cache import cache

RATE_LIMITED_ROUTES = {
    "/api/auth/login/",
    "/api/auth/password-reset/",
}


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in RATE_LIMITED_ROUTES:
            ip = request.META.get("REMOTE_ADDR")
            cache_key = f"rate_limit_{ip}_{request.path}"
            requests_count = cache.get(cache_key, 0)
            if requests_count >= 15:
                return JsonResponse(
                    {"erro": "Muitas requisições. Tente novamente mais tarde."},
                    status=429,
                )
            cache.set(cache_key, requests_count + 1, timeout=300)

        if "api/admin/" in request.path and not request.user.is_authenticated:
            return JsonResponse(
                {"erro": "Autenticação necessária."},
                status=401
            )

        response = self.get_response(request)

        # CORS        
        response["Access-Control-Allow-Origin"] = config(
            "ALLOWED_ORIGIN",
            default="http://localhost:3000",
        )
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        # Segurança
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        
        return response 