from django.db import transaction
from django.db.models import F

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from .models import Video, Like
from .serializers import VideoModelSerializer, VideoDetailModelSerializer
from .permissions import PublishedOrOwnerPermission


class VideoViewSet(ReadOnlyModelViewSet):
    queryset = Video.objects.select_related('owner')
    serializer_class = VideoModelSerializer
    permission_classes = [PublishedOrOwnerPermission, ]

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()

        if request.query_params.get('user_expand') == 'true':
            serialize = VideoDetailModelSerializer(video)
        else:
            serialize = self.get_serializer(video)

        return Response(serialize.data)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def likes(self, request, pk, *args, **kwargs):
        video = self.get_object()
        user = request.user

        if video.owner == user:
            return Response({'error': 'you cant like this video'}, HTTP_400_BAD_REQUEST)

        if Like.objects.filter(user=user, video=video).exists():
            return Response({'error': 'your like are exists'}, HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user, video=video)
        Video.objects.filter(id=video.id).update(total_likes=F('total_likes') + 1)

        return Response({'message': 'like successfully'}, HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def ids(self, request, *args, **kwargs):
        video_ids = self.get_queryset().filter(is_published=True).values_list('id', flat=True)

        return Response(video_ids)
