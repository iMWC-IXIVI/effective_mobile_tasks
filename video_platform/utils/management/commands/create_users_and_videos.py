import random
import shutil

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import F, OuterRef, Subquery, Count
from django.db import transaction

from video_app.models import Video, VideoFile, Like


User = get_user_model()


class Command(BaseCommand):
    help = 'Create 10k users and 100k videos + random likes'

    @transaction.atomic
    def handle(self, *args, **options):
        """Ручка для создания 10к пользователей и 100к видеозаписей с рандомной реализацией лайков"""

        self.stdout.write(f'Created users + videos')

        # Создание 10к пользователей, частичная загрузка через bulk

        butch_users = []
        for index in range(10_000):
            butch_users.append(User(username=f'user_{index}', email=f'user_{index}@main.ru', password=f'user_password_{index}'))

            if len(butch_users) >= 1000:
                User.objects.bulk_create(butch_users)
                butch_users = []

        User.objects.bulk_create(butch_users)

        users = User.objects.all()

        # Создание 100к видео, частичная загрузка через bulk

        butch_videos = []
        for index in range(100_000):
            video = Video(owner=random.choice(users), is_published=random.choice([True, False]), name=f'video name {index}')

            butch_videos.append(video)

            if len(butch_videos) >= 5000:
                Video.objects.bulk_create(butch_videos)
                butch_videos = []

        Video.objects.bulk_create(butch_videos)
        videos = Video.objects.all()

        # Копирование файла, лежащий в fixture_files, req.mp4 (объем на диске 4КБ (обычный req.txt переформатированный в mp4))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~ДОЛГО~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        src_url = settings.BASE_DIR/'fixture_files'/'req.mp4'
        butch_video_files = []
        for index, video in enumerate(videos):
            media_url = settings.MEDIA_ROOT/'videos'/f'video_{index}.mp4'

            shutil.copy(src_url, media_url)
            butch_video_files.append(VideoFile(video=video, file=f'video_{index}.mp4', quality=random.choice(VideoFile.Quality.choices)[0]))

            if len(butch_video_files) >= 2000:
                VideoFile.objects.bulk_create(butch_video_files)
                butch_video_files = []

        VideoFile.objects.bulk_create(butch_video_files)

        # Рандомнное создание лайков из рандомных пользователей с учетом всех условий

        butch_likes = []
        for video in videos:
            print(video.id)
            random_users = random.sample(list(users), k=random.randint(1, 100))
            for random_user in random_users:
                if video.owner == random_user:
                    continue

                butch_likes.append(Like(user=random_user, video=video))

                if len(butch_likes) >= 5000:
                    Like.objects.bulk_create(butch_likes)
                    butch_likes = []

        Like.objects.bulk_create(butch_likes)

        subquery_likes = Like.objects.filter(video=OuterRef('id')).values('video').annotate(count=Count('id')).values('count')
        Video.objects.update(total_likes=Subquery(subquery_likes))

        self.stdout.write(f'Command done, created 10k users, 100k Video and VideoFile, 100k+ likes')
