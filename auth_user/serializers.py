from rest_framework import serializers
from auth_user import constants


class SendSerializer(serializers.Serializer):
    message = serializers.CharField()

    def validate(self, attrs):
        if not self.context.get('user').telegram_id:
            raise serializers.ValidationError(constants.INVALID_TELEGRAM_ID)

        return attrs
