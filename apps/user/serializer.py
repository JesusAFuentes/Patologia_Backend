from rest_framework import serializers
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(
        choices=User.Type.choices, default=User.Type.ADMIN)

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'groups',
                   'user_permissions')
        extra_kwargs = {
            'user_type': {
                'read_only': True
            },
        }
    _mapper = {
        User.Type.ADMIN: (User, 'admins'),
    }
