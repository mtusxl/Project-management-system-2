from rest_framework import serializers

from .models import Column, Dashbord


class DashbordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashbord
        fields = "__all__"


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["name", "order"]
