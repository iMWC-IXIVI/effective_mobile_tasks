from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from .models import Video
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
