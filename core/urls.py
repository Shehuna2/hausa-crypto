from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.PostList, name='home-index'),
    path('about/', views.AboutPage, name='about-page'),
    path('category/<slug:category_slug>/', views.PostList, name='post_category'),
    path('<slug:post>/', views.PostDetail, name='post-detail'),
    path('comment/reply/', views.ReplyComment, name='reply'),
    path('tag/<slug:tag_slug>/', views.PostList, name='post_tag'),
]
