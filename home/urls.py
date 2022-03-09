from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:post_id>/<slug:post_slug>/', views.PostDetaileView.as_view(), name='post_detail'),
    path('comment/reply/<int:post_id>/<int:comment_id>/', views.CreateReplyCommentView.as_view(), name='create_reply_comment'),
    path('post/like/<int:post_id>', views.PostLikeView.as_view(), name='post_like'),
]
