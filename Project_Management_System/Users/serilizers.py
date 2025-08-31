import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from Project_Management_System.config.settings.base import REDIS_CLIENT
from Project_Management_System.Users.signals import verification_code_requested

User = get_user_model()
r_client = REDIS_CLIENT
logger = logging.getLogger(__name__)


class RegistSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
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
        logger.debug(f"Сохранение данных регистрации в Redis для {number}")

        verification_code_requested.send(sender=RegistSerializer, number=number)
        logger.info(f"код отправлен на номер  - {number})")
        return True

    def verify_and_create(self, number, code):
        store_code = r_client.get(f"verify_code:{number}")
        logger.info(f"код получен по номеру  - {number}, код: {store_code})")
        store_data = r_client.get(f"reg_data:{number}")
        logger.debug(f"Получение данных регистрации из Redis для {number}: {store_data}")

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

        logger.info(f"Удаление данных из Redis для {number} после создания пользователя")
        r_client.delete(f"reg_data:{number}", f"verify_code:{number}")
        return user
