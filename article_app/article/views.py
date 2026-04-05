from django.views.generic import ListView, DetailView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status=Article.Status.PUBLISHED)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
