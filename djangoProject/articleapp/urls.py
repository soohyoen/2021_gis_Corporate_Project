from django.urls import path

from articleapp.views import  ArticleListView

app_name = 'articleapp'

urlpatterns = [
    path('list/', ArticleListView.as_view(), name='list')
    ]