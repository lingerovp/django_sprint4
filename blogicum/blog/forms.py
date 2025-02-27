from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        # Так она же автоматом и встает, формат тут не влияет же.
        # После первого ревью не вставала,
        # потому что я забыл убрать не нужную константну из настроек,
        # эту - DATETIME_INPUT_FORMATS = ['%d-%Y-%m %H:%M'].
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
