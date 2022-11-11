from rest_framework import authentication

from organization.models import User


class WxAuthBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        if username := request.META.get('HTTP_X_WX_OPENID'):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=username)
            return user, None
        return None
