from django import template
from ..models import Post
from  django.db.models import Count

register = template.Library()

@register.simple_tag()
def total_posts():
    #return Post.published.name
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_psts(count=3):
    latest_post = Post.published.order_by('-publish')[:count]
    return {'latest_post':latest_post}
