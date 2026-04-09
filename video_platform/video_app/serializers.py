from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Video


class VideoModelSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'name', 'created_at', 'owner_id']


class VideoDetailModelSerializer(ModelSerializer):
    owner = SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'name', 'created_at', 'owner']

    def get_owner(self, obj):
        return {
            'id': obj.owner.id,
            'username': obj.owner.username
        }
