from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') #Указываем какие поля отображать в превью
    list_filter = ('status', 'created', 'publish', 'author') #Добавляем фильтр в админке справа
    search_fields = ('title', 'body') #Добавляем строку поиска и указываем параметры поиска
    prepopulated_fields = {'slug' : ('title',)} #Для автоматического заполнения slug при добавлении новой статьи
    raw_id_fields = ('author',) #Добавляем возможность выбора автора из существующих (автоматом подставляем user id)
    date_hierarchy = 'publish'  #Добавляем вывод публикаций по дате(навигация по дате) (удобная фильтрация за день или за весь год)
    ordering = ('status', 'publish') #Сортировка по умолчанию по статусу

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

# Register your models here.
