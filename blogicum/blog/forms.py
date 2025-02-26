from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        # Не указываю тут формат, т.к. в этом нет смысла
        # datetime-local на выходе всегда возвращает формат YYYY-MM-DDTHH:mm
        # а уже в зависимости от настроек браузера,
        # в проде у всех дата будет своя.
        # Возможно, я просто тебя не правильно понял тут.
        # Обсуждали этот вопрос с наставником
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
