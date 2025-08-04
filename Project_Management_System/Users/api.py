from rest_framework import permissions, status
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serilizers import RegistSerializer


class RegistAPI(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = request.data.get("code")

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

            serializer.request_code(serializer.validated_data)
            return Response(
                {
                    "message": f"Код отправлен на номер {serializer.validated_data["number"]}"  # noqa: E501
                }
            )


# проверить код
