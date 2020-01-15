from django import forms

#Создадим класс формы, унаследованный от встроенного базавого класса Django стандартных форм Form
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea) #Заменили стандартный input на <text-area>