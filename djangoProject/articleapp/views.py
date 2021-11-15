# Create your views here.
from django.views.generic import ListView

from articleapp.models import Article


class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articleapp/home.html'
    paginate_by = 20