import logging

from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken
from waffle import flag_is_active

from Project_Management_System.config.settings.base import REDIS_CLIENT

from .models import User
from .serilizers import RegistSerializer

r_client = REDIS_CLIENT
logger = logging.getLogger(__name__)


class RegistAPI(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegistSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            code = request.data.get("code")
        except ValidationError as e:
            return Response(
                {"Validation error error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if code:
                user = serializer.verify_and_create(
                    number=serializer.validated_data["number"], code=code
                )
                refresh = RefreshToken.for_user(user=user)
                return Response(
                    {"access": str(refresh.access_token), "refresh_token": str(refresh)},
                    status=status.HTTP_201_CREATED,
                )
            else:

                if serializer.request_code(serializer.validated_data):
                    return Response(
                        {
                            "message": f"Код отправлен на номер {serializer.validated_data["number"]}"  # noqa: E501
                        }
                    )
                else:
                    return Response({"error": "код не отправлен, ошибка задачи celery"})
        except ValidationError as e:
            return Response(
                {"Validation error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response({"Value error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Test_API(APIView):
    def get(self, requset):
        if flag_is_active(requset, "test_flag"):
            return Response({"data": "new data"}, status=status.HTTP_200_OK)
        else:
            return Response({"data": "old_data"}, status=status.HTTP_200_OK)
