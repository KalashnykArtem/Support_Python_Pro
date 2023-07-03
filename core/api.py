import json
from typing import Callable

from django.http import HttpResponse, JsonResponse

from core.errors import SerializerError
from core.models import User

# from core.serializers import UserCreateSerializer, UserPublicSerializer
from core.serializers import UserCreateRequestSerializer  # isort:skip
from core.serializers import UserCreateResponseSerializer  # isort:skip


def base_error_handler(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SerializerError as error:
            message = {"errors": error._serializer.errors}
            status_code = 400
        except Exception as error:
            message = {"error": str(error)}
            status_code = 500

        return HttpResponse(
            content_type="application/json",
            content=json.dumps(message),
            status=status_code,
        )

    return inner


@base_error_handler
def create_user(request):
    if request.method != "POST":
        raise ValueError("Only POST method is allowed")

    # user_create_serializer = UserCreateSerializer(
    #     data=json.loads(request.body)
    # )  # noqa: E501
    user_create_serializer = UserCreateRequestSerializer(
        data=json.loads(request.body)
    )  # noqa: E501
    is_valid = user_create_serializer.is_valid()
    if not is_valid:
        raise SerializerError(user_create_serializer)

    user = User.objects.create_user(**user_create_serializer.validated_data)
    # user_public_serializer = UserPublicSerializer(user)
    user_public_serializer = UserCreateResponseSerializer(user)

    return JsonResponse(user_public_serializer.data)
