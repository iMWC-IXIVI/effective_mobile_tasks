from django.urls import path

from .views import ArticleListView, ArticleDetailView


urlpatterns = [
    path('get-list/', ArticleListView.as_view(), name='article_list'),
    path('get-detail/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
]
