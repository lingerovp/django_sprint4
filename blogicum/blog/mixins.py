from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Comment, Post


class TestMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.get_object().author == self.request.user


class CommentTestAndUrlMixin(TestMixin):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs.get('pk')}
        )


class PostTestAndEdit(TestMixin):
    model = Post
    template_name = 'blog/create.html'
