from django import forms
from .models import Comment

#Создадим класс формы, унаследованный от встроенного базавого класса Django стандартных форм Form
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Ваше имя')
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea) #Заменили стандартный input на <text-area>

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body') #Определяем какие поля модели используем