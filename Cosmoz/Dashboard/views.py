from .models import Post
from .forms import PostForm
from django.shortcuts import render, redirect
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import PostForm, CommentForm
from .models import Post, Comments
from Cosmoz import settings
from django.shortcuts import get_object_or_404
from froala_editor import views as froala_views
import uuid
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string
import shutil


def directory(Post):

    DirectoryPath = f"{Post.Author}/Posts/{Post.PostID}.jpg"
    # return str(settings.BASE_DIR.joinpath(DirectoryPath))        print("From Post ",DirectoryPath)
    return DirectoryPath


# Create your views here.


def DashboardView(request):
    user = request.user
    if user.is_authenticated:
        objects = Post.objects.all()
        liked = False
        for post in objects:
            total_likes = post.total_likes()
            liked = False
            if post.likes.filter(email=request.user.email).exists():
                liked = True
        return render(
            request,
            "Dashboard/Dashboard.html",
            {"object_list": objects, "liked": liked},
        )
    else:
        return HttpResponseRedirect(reverse("Login"))


def PostCreate(request):
    if request.method == "POST":
        PostDetails = PostForm(request.POST, request.FILES)
        NewPost = Post()
        NewPost = PostDetails.save(commit=False)
        author = request.user
        NewPost.Author = author
        NewPost.save()
        return HttpResponseRedirect(reverse("Dashboard-view"))
    return render(request, "Dashboard/PostCreate.html", {"form": PostForm})


def PostEdit(request, post_id):
    post = Post.objects.get(PostID=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            url = reverse("Post-view", kwargs={"post_id": post.PostID})
            return render(request, "Dashboard/EditDone.html", {"url": url})
        else:
            form = PostForm(instance=post)
    else:
        form = PostForm(instance=post)
    return render(request, "Dashboard/PostEdit.html", {"form": form, "post": post})


def PostDelete(request, post_id):
    post = Post.objects.get(PostID=post_id)
    post.delete()
    return render(request, "Dashboard/DeleteDone.html")


def PostUpdate(request):
    return render(request, "Dashboard/PostUpdate.html")


def PostView(request, post_id):
    # print(post_id)
    DisplayObject = Post.objects.get(PostID=post_id)
    DisplayComments = Comments.objects.filter(post=post_id)
    return render(
        request,
        "Dashboard/PostView.html",
        {
            "post": DisplayObject,
            "comments": DisplayComments,
            "commentform": CommentForm,
        },
    )


def CommentView(request, post_id):
    post = get_object_or_404(Post, PostID=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        NewComment = Comments()
        NewComment = form.save(commit=False)
        NewComment.post = post
        author = request.user
        NewComment.Author = author
        NewComment.save()
        return HttpResponseRedirect(reverse("Dashboard-view"))
    else:
        form = CommentForm()
    return render(request, "Dashboard/AddComments.html", {"form": form})


def CommentEdit(request, post_id, comments_id):
    post = get_object_or_404(Post, PostID=post_id)
    comments = get_object_or_404(Comments, CommentsID=comments_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comments)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("Post-view", kwargs={"post_id": post.PostID})
            )
            # url = reverse(
            #     'Post-view', kwargs={'post_id': post_id, 'comments_id': comments_id})
            # return render(request, 'Dashboard/EditDone.html', {'url': url})
        else:
            form = CommentForm(instance=comments)
    else:
        form = CommentForm(instance=comments)
    return render(
        request, "Dashboard/CommentEdit.html", {"form": form, "comment": comments}
    )


def CommentDelete(request, post_id, comment_id):
    post = get_object_or_404(Post, PostID=post_id)
    comment = Comments.objects.get(CommentsID=comment_id)
    comment.delete()
    return render(request, "Dashboard/DeleteDone.html")


def LikeView(request, post_id):
    post = get_object_or_404(Post, PostID=post_id)
    liked = False
    if post.likes.filter(email=request.user.email).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        liked = True
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse("Dashboard-view"))
