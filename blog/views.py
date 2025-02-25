from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank #Последние два позволяют ранжировать выдачу
from django.contrib.postgres.search import TrigramSimilarity

def post_list(request, tag_slug=None):
    #posts = Post.published.all() #Используем свой менеджер
    object_list = Post.published.all()
    tag=None

    if tag_slug:
        tag = get_object_or_404(Tag, tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page, 'posts':posts, 'tag':tag})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post =get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
            .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                        .order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post':post,
                                                     'comments':comments,
                                                     'new_comment':new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts':similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published') #Получение статьи по id
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST) #Отправка формы на сохранение
        if form.is_valid(): # Если все поля корректно заполнены, то сохраняем форму
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) рекомендую крутые статьи "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Прочесть "{}" можно здесь {}\n\n{} прокомментировал:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'vetalboy94@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        search_query = SearchQuery(query)
        results = Post.objects.annotate(
            similarity=TrigramSimilarity('title', query),
        ).filter(similarity__gt=0.3).order_by('-similarity')
        # results = Post.objects.annotate(
        #     search=search_vector,
        #     rank=SearchRank(search_vector, search_query)
        # ).filter(rank__gte=0.3).order_by('-rank') #Отображаем ранжированные статьи с весом более 0,3
        # Простой вариант
        # results = Post.objects.annotate(
        #     search=SearchVector('title', 'body'),
        # ).filter(search=query)
    return render(request, 'blog/post/search.html', {'form':form,
                                                     'query':query,
                                                     'results':results})