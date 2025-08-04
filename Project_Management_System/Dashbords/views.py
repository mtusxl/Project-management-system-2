from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Column, Dashbord
from .serializers import ColumnSerializer, DashbordSerializer


class DashbordAPI(viewsets.ModelViewSet):
    serializer_class = DashbordSerializer
    queryset = Dashbord.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Dashbord.objects.filter(
            Q(project__author=user) | Q(project__members=user)
        ).distinct()

    @action(detail=True, methods=["POST"], url_path="columns")
    def add_column(self, request, pk=None):
        try:
            dashbord = Dashbord.objects.get(pk=pk)
            # column_name = request.data.get("name")
            # order = request.data.get("order", 0)
            if dashbord:
                serializer = ColumnSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(dashbord=dashbord)
                return Response(
                    {"status": "Column added", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
        except Dashbord.DoesNotExist:
            return Response(
                {"error": "Board not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["PUT"], url_path="columns/(?P<column_id>[^/.]+)")
    def update_column(self, request, pk=None, column_id=None):
        try:
            dashboard = Dashbord.objects.get(pk=pk)
            column = Column.objects.get(pk=column_id, dashbord=dashboard)

            if column:

                serializer = ColumnSerializer(column, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {"status": "Column updated", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )

        except Column.DoesNotExist:
            return Response(
                {"error": "Column not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
