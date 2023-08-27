from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "email" : user.email,
        "full_name" : f'{user.first_name} {user.last_name}',
        "user" : user.get_user_type_display(),
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }