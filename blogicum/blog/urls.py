from django.urls import include, path

from . import views

app_name = 'blog'

profile = [
    path('edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('<slug:username>/', views.ProfileListView.as_view(), name='profile'),
]

posts = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path(
        '<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        '<int:pk>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        '<int:pk>/edit_comment/<int:comment_id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        '<int:pk>/delete_comment/<int:comment_id>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostListView.as_view(),
        name='category_posts',
    ),
    path('profile/', include(profile)),
    path('posts/', include(posts)),
]
