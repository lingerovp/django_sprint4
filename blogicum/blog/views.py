from datetime import datetime as dt

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm, PostForm, ProfileForm
from .mixins import CommentTestAndUrlMixin, PostTestAndEdit
from .models import Category, Comment, Post, User
from common.constants import PAGINATE_BY


def filter_published_posts(queryset):
    return (
        queryset.select_related('location', 'category', 'author')
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=dt.now(),
        )
    )


def comment_annotate(queryset):
    return (
        queryset
        .annotate(comment_count=Count('comment'))
        .order_by('-pub_date')
    )


class IndexListView(ListView):
    model = Post
    queryset = comment_annotate(filter_published_posts(Post.objects))
    template_name = 'blog/index.html'
    paginate_by = PAGINATE_BY


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        self.category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True,
        )
        return comment_annotate(filter_published_posts(self.category.post))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileListView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self, queryset=None):
        author = get_object_or_404(User, username=self.kwargs['username'])
        post_list = filter_published_posts(author.post)
        if self.request.user == author:
            post_list = (
                author
                .post
                .select_related('location', 'category', 'author')
            )
        return comment_annotate(post_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'],
        )
        return context


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.get_object() == self.request.user

    def get_object(self, queryset=None):
        return self.request.user


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            filter_published_posts(Post.objects),
            pk=pk
        )

    def get_queryset(self, queryset=None):
        author = get_object_or_404(User, username=self.kwargs['username'])
        post_list = filter_published_posts(author.post)
        if self.request.user == author:
            post_list = author.post.all()
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comment.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.author.username}
        )


class PostUpdateView(PostTestAndEdit, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs.get('pk')}
        )

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(reverse(
                'blog:post_detail',
                kwargs={'pk': post.pk},
            ))
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(PostTestAndEdit, DeleteView):
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comments.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs.get('pk')}
        )


class CommentUpdateView(CommentTestAndUrlMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentTestAndUrlMixin, DeleteView):
    pass
