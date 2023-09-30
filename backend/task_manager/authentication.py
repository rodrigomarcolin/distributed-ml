from rest_framework import authentication
from rest_framework import exceptions
from .models import Cliente


class BearerTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.META.get("HTTP_AUTHORIZATION")

        if not authorization_header:
            return None

        # Split the Authorization header to extract the token
        parts = authorization_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
        else:
            return None

        try:
            api_key_obj = Cliente.objects.get(key=token)
        except Cliente.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid API key")

        return api_key_obj, token
