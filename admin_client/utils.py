
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .models import CustomUser, Permision, RolePermision


def generate_tokens(user):

    access_payload = {
        "user_id": user.id,
        "token_type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    refresh_payload = {
        "user_id": user.id,
        "token_type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }

    access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        refresh_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "access": access_token,
        "refresh": refresh_token
    }


def verify_token(token, token_type):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        if payload.get("token_type") != token_type:
            return None

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


def get_user_from_token(token):

    payload = verify_token(token, "access")

    if not payload:
        return None

    try:
        user = CustomUser.objects.get(
            id=payload["user_id"],
            is_active=True
        )
        return user

    except (CustomUser.DoesNotExist, KeyError):
        return None


def generate_access_token(user_id):

    payload = {
        "user_id": user_id,
        "token_type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token


def has_permission(user, permission_name):

    try:
        permission = Permision.objects.get(
            permision_name=permission_name
        )

        return RolePermision.objects.filter(
            role=user.role,
            permision=permission
        ).exists()

    except Permision.DoesNotExist:
        return False
