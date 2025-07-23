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
        user = serializer.save()

        refresh = RefreshToken.for_user(user=user)
        return Response(
            {"access": str(refresh.access_token), "refresh_token": str(refresh)},
            status=status.HTTP_201_CREATED,
        )
