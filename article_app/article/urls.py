from django.urls import path

from .views import ArticleListView


urlpatterns = [
    path('get-list/', ArticleListView.as_view(), name='article_list')
]
