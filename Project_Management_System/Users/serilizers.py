from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegistSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("number", "password")

    def create(self, validated_data):
        user = User.objects.create(
            number=validated_data["number"],
        )
        user.set_password(validated_data["number"])
        user.save()
        return user
