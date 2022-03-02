from django.urls import path, include
from . import views
from froala_editor import views as froala_views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.ForumView, name="Forum-view"),
    path("addquestion", views.QuestionPost, name="QuestionPost-view"),
    path("<uuid:ques_id>", views.QuestionView, name="Question-view"),
    path("<uuid:ques_id>/editquestion", views.QuestionEdit, name="QuestionEdit-view"),
    path(
        "<uuid:ques_id>/deletequestion",
        views.QuestionDelete,
        name="QuestionDelete-view",
    ),
    path("<uuid:ques_id>/answer", views.AnswerView, name="Answer-view"),
    path(
        "<uuid:ques_id>/editanswer/<uuid:answer_id>",
        views.AnswerEdit,
        name="Answer-edit",
    ),
    path(
        "<uuid:ques_id>/deleteanswer/<uuid:answer_id>",
        views.AnswerDelete,
        name="Answer-delete",
    ),
    path("froala_editor/", include("froala_editor.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("<uuid:ques_id>/<uuid:answer_id>/like", views.LikeView, name="like_post"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
