from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

#Добавляем свой менеджер (пока что просто так)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published') #Фильтр по умолчанию по опубликованным статьям

class Post(models.Model):
    objects = models.Manager() #Это мнеджер по умолчанию
    published = PublishedManager() # А это самоельный менеджер выше
    #Post.published.filter(title__startswith='Who') Т.е. при выполнении этой команды мы получим не только статьи, начинающиеся на Who, но и опубликованные
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #Чтобы обратиться не comment_set, a comment
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # Чтобы можно было скрыть коммент(непреемлемый, например)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Кометарий {} к статье {}'

# class Comment(models.Model):
#     post = models.ForeignKey(Post,
#                              on_delete=models.CASCADE,
#                              related_name='comments')
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)
#
#     class Meta:
#         ordering = ('created',)
#
#     def __str__(self):
#         return 'Comment by {} on {}'.format(self.name, self.post)