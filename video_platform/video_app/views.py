from django.db import transaction
from django.db.models import F, OuterRef, Subquery, Count

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from .models import Video, Like
from .serializers import VideoModelSerializer, VideoDetailModelSerializer
from .permissions import PublishedOrOwnerPermission


class VideoViewSet(ReadOnlyModelViewSet):
    serializer_class = VideoModelSerializer
    permission_classes = [PublishedOrOwnerPermission, ]

    def get_queryset(self):
        """Замена стандартного queryset для правильного отображения списка видео"""

        if self.action == 'list':
            return Video.objects.select_related('owner').filter(is_published=True)
        return Video.objects.select_related('owner')

    def retrieve(self, request, *args, **kwargs):
        """Переопределение детальной информации о видео"""

        video = self.get_object()

        if request.query_params.get('user_expand') == 'true':
            serialize = VideoDetailModelSerializer(video)
        else:
            serialize = self.get_serializer(video)

        return Response(serialize.data)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def likes(self, request, pk, *args, **kwargs):
        """Создание лайков на видео (атомарно)"""

        video = self.get_object()
        user = request.user

        if user.is_anonymous:
            return Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)

        if video.owner == user:
            return Response({'error': 'you cant like this video'}, HTTP_400_BAD_REQUEST)

        if Like.objects.filter(user=user, video=video).exists():
            return Response({'error': 'your like are exists'}, HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user, video=video)
        Video.objects.filter(id=video.id).update(total_likes=F('total_likes') + 1)

        return Response({'message': 'like successfully'}, HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def ids(self, request, *args, **kwargs):
        """Вывод всех идентификаторов опубликованных видео"""

        video_ids = self.get_queryset().filter(is_published=True).values_list('id', flat=True)
        return Response(video_ids)

    @action(detail=False, methods=['get'], url_path='statistics-subquery')
    def statistics_subquery(self, request, *args, **kwargs):
        """Сбор лайков по видео через подзапрос"""

        likes_query = Like.objects.filter(video=OuterRef('id')).values('video').annotate(likes_count=Count('id')).values('likes_count')
        videos = Video.objects.annotate(likes_count=Subquery(likes_query)).values('id', 'likes_count')
        return Response(videos)

    @action(detail=False, methods=['get'], url_path='statistics-group-by')
    def statistics_group_by(self, request, *args, **kwargs):
        """Сбор лайков по видео через группировку"""

        videos = Video.objects.annotate(likes_total=Count('like')).values('id', 'likes_total')
        return Response(videos)
