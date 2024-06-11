from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
)
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from knox.views import LoginView
import base64
import binascii


class UserViewSet(viewsets.GenericViewSet):
    """
    Basic Generic viewset for now
    """

    @action(detail=False, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def update_password(self, request):
        serializer = self.get_serializer(instance=request.user,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': _('Password has been changed.')})


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class CustomBasicAuthentication(BasicAuthentication):
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            self.raise_invalid_credentials()
        elif len(auth) > 2:
            self.raise_invalid_credentials()

        try:
            auth_decoded = base64.b64decode(auth[1]).decode('utf-8')
        except (UnicodeDecodeError, binascii.Error):
            self.raise_invalid_credentials()

        auth_parts = auth_decoded.partition(':')
        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=auth_parts[0])
        except ObjectDoesNotExist:
            self.raise_invalid_credentials()

        if user.is_active:
            return self.authenticate_credentials(auth_parts[0], auth_parts[2],
                                                 request)
        else:
            self.raise_invalid_credentials(_('User is currently banned'))

    def authenticate_credentials(self, userid, password, request=None):
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            self.raise_invalid_credentials(_('Invalid username/password.'))

        if not user.is_active:
            self.raise_invalid_credentials(_('User inactive or deleted.'))

        return (user, None)

    def raise_invalid_credentials(self, message=_('Invalid credentials.')):
        raise exceptions.AuthenticationFailed(
            message, code=status.HTTP_401_UNAUTHORIZED)


class LoginCustomView(LoginView):
    """
    This only overrides the original View for using the Basic Authentication
    instead of the default one
    """
    authentication_classes = (CustomBasicAuthentication,)
