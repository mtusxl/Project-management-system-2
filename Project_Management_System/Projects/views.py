from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.cache_utils import cache_api

from .models import Project
from .serializers import ProjectSerializer


class ProjectAPI(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects.filter(Q(author=user) | Q(members=user))
            .prefetch_related("members")
            .select_related("author")
            .distinct()
        )

    @method_decorator(cache_api(prefix="project"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_api(prefix="project-detail"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=["POST"], url_path="members")
    def add_member(self, request, pk=None):
        projects = self.get_object()
        user_id = request.data.get("user_id")
        if user_id:
            projects.members.add(user_id)
            return Response(
                {"status": "Member added in project"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["DELETE"], url_path="members/(?P<user_id>[^/.]+)")
    def del_member(self, request, pk=None, user_id=None):
        try:
            projects = self.get_object()
            projects.members.remove(user_id)
            return Response(
                {"status": "Member remove from project"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
