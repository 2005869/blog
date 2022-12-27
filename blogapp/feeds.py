from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from . import models


class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('blogapp:post_list')
    description = 'New posts of my blog'

    def items(self):
        return models.Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)