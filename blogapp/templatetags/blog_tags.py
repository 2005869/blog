import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from .. import models


register = template.Library()


@register.simple_tag
def total_posts():
    return models.Post.published.count()


@register.inclusion_tag('blogapp/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = models.Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return models.Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))