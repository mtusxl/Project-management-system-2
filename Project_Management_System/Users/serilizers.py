import json

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from Project_Management_System.settings.base import REDIS_CLIENT

from .signals import verification_code_requested

User = get_user_model()
r_client = REDIS_CLIENT


class RegistSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("number", "username", "password")

    def request_code(self, validated_data):
        number = validated_data["number"]
        if User.objects.filter(number=number).exists():
            raise serializers.ValidationError(
                {"error": "A user with this phone number is already in the system!"}
            )

        r_client.set(f"reg_data:{number}", json.dumps(validated_data), ex=300)
        verification_code_requested.send(sender=RegistSerializer, number=number)
        return {"message": "Code sent to your number."}

    def verify_and_create(self, number, code):
        store_code = r_client.get(f"verify_code:{number}")
        store_data = r_client.get(f"reg_data:{number}")

        if not store_data:
            raise serializers.ValidationError(
                {"munber": "No registration data found or expired."}
            )
        if int(store_code) != int(code):
            raise serializers.ValidationError({"code": "Invalid or expired code."})

        validated_data = json.loads(store_data)
        user = User.objects.create(
            number=validated_data["number"], username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()

        r_client.delete(f"reg_data:{number}", f"verify_code:{number}")
        return user
