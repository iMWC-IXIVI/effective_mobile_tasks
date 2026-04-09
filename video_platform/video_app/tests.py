from django.contrib.auth import get_user_model
from django.db.models import F

from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from .models import Video, Like


User = get_user_model()


class VideoTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='UserTest',
            password='usertest',
            email='usertest@co.m'
        )

        self.true_published_video = Video.objects.create(
            owner=self.user,
            is_published=True,
            name='Publish name'
        )

        self.false_published_video = Video.objects.create(
            owner=self.user,
            name='Not publish name'
        )

    def test_get_published_video(self) -> None:
        name_fields = {'id', 'name', 'created_at', 'owner_id'}
        response = self.client.get('/v1/videos/')

        if isinstance(response.data, dict):
            videos = response.data.get('results')
        elif isinstance(response.data, list):
            videos = response.data

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(videos), 2)

        for video in videos:
            self.assertEqual(set(video.keys()), name_fields)

    def test_detail_login_videos(self) -> None:
        fields_name = {'id', 'name', 'created_at', 'owner_id'}

        self.client.login(username='UserTest', password='usertest')

        videos = [
            self.client.get(f'/v1/videos/{self.true_published_video.id}/'),
            self.client.get(f'/v1/videos/{self.false_published_video.id}/')
        ]
        status_codes = list(map(lambda video: video.status_code, videos))
        videos_fields = list(map(lambda video: set(video.data.keys()), videos))

        self.assertEqual(status_codes, [HTTP_200_OK, HTTP_200_OK])
        for video_fields in videos_fields:
            self.assertEqual(video_fields, fields_name)

    def test_detail_login_videos_expand(self) -> None:
        fields_name = {'id', 'name', 'created_at', 'owner'}

        self.client.login(username='UserTest', password='usertest')

        videos = [
            self.client.get(f'/v1/videos/{self.true_published_video.id}/?user_expand=true'),
            self.client.get(f'/v1/videos/{self.false_published_video.id}/?user_expand=true')
        ]

        status_codes = list(map(lambda video: video.status_code, videos))
        videos_fields = list(map(lambda video: set(video.data.keys()), videos))

        self.assertEqual(status_codes, [HTTP_200_OK, HTTP_200_OK])
        for video_fields in videos_fields:
            self.assertEqual(video_fields, fields_name)

    def test_detail_logout_videos(self) -> None:
        fields_name = {'id', 'name', 'created_at', 'owner_id'}

        videos = [
            self.client.get(f'/v1/videos/{self.true_published_video.id}/'),
            self.client.get(f'/v1/videos/{self.false_published_video.id}/')
        ]
        status_codes = list(map(lambda video: video.status_code, videos))
        videos_fields = list(map(lambda video: set(video.data.keys()), videos))

        self.assertEqual(status_codes, [HTTP_200_OK, HTTP_401_UNAUTHORIZED])
        for index, video_fields in enumerate(videos_fields):
            if status_codes[index] != HTTP_401_UNAUTHORIZED:
                self.assertEqual(video_fields, fields_name)

    def test_detail_logout_videos_expand(self) -> None:
        fields_name = {'id', 'name', 'created_at', 'owner'}

        videos = [
            self.client.get(f'/v1/videos/{self.true_published_video.id}/?user_expand=true'),
            self.client.get(f'/v1/videos/{self.false_published_video.id}/?user_expand=true')
        ]
        status_codes = list(map(lambda video: video.status_code, videos))
        videos_fields = list(map(lambda video: set(video.data.keys()), videos))

        self.assertEqual(status_codes, [HTTP_200_OK, HTTP_401_UNAUTHORIZED])
        for index, video_fields in enumerate(videos_fields):
            if status_codes[index] != HTTP_401_UNAUTHORIZED:
                self.assertEqual(video_fields, fields_name)


class VideoLikeTestCase(APITestCase):
    def setUp(self) -> None:
        self.main_user = User.objects.create_user(
            username='UserTest',
            password='usertest',
            email='usertest@co.m'
        )

        self.user = User.objects.create_user(
            username='UserTest2',
            password='usertest2',
            email='usertest2@co.m'
        )

        self.video = Video.objects.create(
            owner=self.main_user,
            name='video name',
            is_published=True
        )

    def test_detail_video_like_yourself(self) -> None:
        self.client.login(username='UserTest', password='usertest')

        response = self.client.post(f'/v1/videos/{self.video.id}/likes/')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'you cant like this video')

    def test_detail_video_like(self) -> None:
        self.client.login(username='UserTest2', password='usertest2')

        response = self.client.post(f'/v1/videos/{self.video.id}/likes/')

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'like successfully')

    def test_detail_video_like_unauthorized(self) -> None:
        response = self.client.post(f'/v1/videos/{self.video.id}/likes/')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Unauthorized')


class AnotherVideoTestCase(APITestCase):
    def setUp(self) -> None:
        users = [
            User.objects.create_user(username='UserTest', password='usertest'),
            User.objects.create_user(username='Test1', password='test1'),
            User.objects.create_user(username='Test2', password='test2')
        ]

        videos = [
            Video.objects.create(owner=users[0], name='Video1', is_published=True),
            Video.objects.create(owner=users[1], name='Video2', is_published=True),
            Video.objects.create(owner=users[2], name='Video3')
        ]

        Like.objects.create(user=users[0], video=videos[1])
        Video.objects.filter(id=videos[1].id).update(total_likes=F('total_likes') + 1)

        Like.objects.create(user=users[1], video=videos[0])
        Video.objects.filter(id=videos[0].id).update(total_likes=F('total_likes') + 1)

        Like.objects.create(user=users[2], video=videos[1])
        Video.objects.filter(id=videos[1].id).update(total_likes=F('total_likes') + 1)

        self.video_likes = Video.objects.all().values_list('total_likes', flat=True)

    def test_check_ids(self) -> None:
        with self.assertNumQueries(1):
            response = self.client.get('/v1/videos/ids/')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_check_statistics_subquery(self) -> None:
        fields_name = {'id', 'likes_count'}
        with self.assertNumQueries(1):
            response = self.client.get('/v1/videos/statistics-subquery/')
        likes = list(map(lambda stat: stat['likes_count'] if stat['likes_count'] else 0, response.data))

        data_fields = list(map(lambda video: set(video.keys()), response.data))

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(likes, list(self.video_likes))

        for data_field in data_fields:
            self.assertEqual(data_field, fields_name)

    def test_check_statistics_group_by(self) -> None:
        fields_name = {'id', 'likes_total'}
        with self.assertNumQueries(1):
            response = self.client.get('/v1/videos/statistics-group-by/')

        data_fields = list(map(lambda video: set(video.keys()), response.data))

        self.assertEqual(response.status_code, HTTP_200_OK)

        for data_field in data_fields:
            self.assertEqual(data_field, fields_name)
