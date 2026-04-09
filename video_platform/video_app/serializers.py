from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Video


class VideoModelSerializer(ModelSerializer):
    """Основной сериализатор для модели Video"""

    class Meta:
        model = Video
        fields = ['id', 'name', 'created_at', 'owner_id']


class VideoDetailModelSerializer(ModelSerializer):
    """Сериализатор для отдачи video detail при ?user_expand"""

    owner = SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'name', 'created_at', 'owner']

    def get_owner(self, obj):
        """Поле для отображения данных о пользователе"""

        return {
            'id': obj.owner.id,
            'username': obj.owner.username
        }
