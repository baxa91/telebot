from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views
from rest_framework.response import Response

from auth_user import service, serializers, constants


class SendTelegramView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=serializers.SendSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.SendSerializer(
            data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)
        service.send_message(self.request.user, serializer.validated_data['message'])
        return Response({'success': constants.SUCCESS})
