from django import template
from ..models import Post
from  django.db.models import Count

register = template.Library()

@register.simple_tag()
def total_posts():
    #return Post.published.name
    return Post.published.count()