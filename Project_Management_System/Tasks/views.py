from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskApi(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(author=user) | Q(executor=user)).distinct()

    @action(detail=True, methods=["POST"], url_path="move/")
    def move_task(self, request, pk=None):
        try:
            task = self.get_object()
            seriaizer = TaskSerializer(task, data=request.data, pertial=True)
            seriaizer.is_valid(raise_exception=True)
            seriaizer.save()
            return Response({"status": "task moved"}, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({"error": str(e)})

    @action(detail=True, methods=["POST"], url_path="assign")
    def assign(self, request, pk=None):
        try:
            task = self.get_object()
            seriaizer = TaskSerializer(task, data=request.data, pertial=True)
            seriaizer.is_valid(raise_exception=True)
            seriaizer.save()
            return Response({"status": "executor assigned"}, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({"error": "Task not found"})

        except Exception as e:
            return Response({"error": str(e)})

    @action(detail=True, methods=["POST"], url_path="subtasks")
    def add_subtask(self, request, pk=None):
        try:
            task = self.get_object()
            seriaizer = TaskSerializer(task, data=request.data, pertial=True)
            seriaizer.is_valid(raise_exception=True)
            seriaizer.save()
            return Response({"status": "subtask added"}, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({"error": "Task not found"})

        except Exception as e:
            return Response({"error": str(e)})
