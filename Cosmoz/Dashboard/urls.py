from django.urls import path, include
from . import views
from froala_editor import views as froala_views
from django.conf.urls import url


urlpatterns = [
    path("", views.DashboardView, name="Dashboard-view"),
    path("newpost", views.PostCreate, name="PostCreate-view"),
    path("<uuid:post_id>", views.PostView, name="Post-view"),
    path("<uuid:post_id>/editpost", views.PostEdit, name="PostEdit-view"),
    path("<uuid:post_id>/deletepost", views.PostDelete, name="PostDelete-view"),
    path("<uuid:post_id>/comments", views.CommentView, name="Comment-view"),
    path(
        "<uuid:post_id>/comments/<uuid:comments_id>",
        views.CommentEdit,
        name="Comment-edit",
    ),
    path(
        "<uuid:post_id>/deletecomment/<uuid:comment_id>",
        views.CommentDelete,
        name="Comment-delete",
    ),
    path("froala_editor/", include("froala_editor.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("like/<uuid:post_id>", views.LikeView, name="like_post"),
]
