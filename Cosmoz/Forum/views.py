from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from Cosmoz import settings
from django.shortcuts import get_object_or_404
from froala_editor import views as froala_views
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string
from django.contrib import messages
from itertools import chain
from django.views.generic import ListView
import uuid
import os
import shutil


def ForumView(request):
    user = request.user
    if user.is_authenticated:
        questions = Question.objects.all()
        context = {}
        context["QnA"] = []
        for question in questions:
            answer = Answer.objects.filter(question_id=question)
            context["QnA"].append({"question": question, "answer": answer})
        return render(request, "Forum/Forum.html", context)
    else:
        return HttpResponseRedirect(reverse("Login"))


def QuestionPost(request):
    if request.method == "POST":
        QuestionDetails = QuestionForm(request.POST, request.FILES)
        print(True)
        NewQuestion = Question()
        NewQuestion = QuestionDetails.save(commit=False)
        author = request.user
        NewQuestion.Author = author
        NewQuestion.save()
        return HttpResponseRedirect(reverse("Forum-view"))
    return render(request, "Forum/QuestionPost.html", {"form": QuestionForm})


def QuestionEdit(request, ques_id):
    question = Question.objects.get(QuestionID=ques_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            url = reverse("Question-view", kwargs={"ques_id": question.QuestionID})
            return HttpResponseRedirect(
                reverse("Question-view", kwargs={"ques_id": question.QuestionID})
            )

            # return HttpResponseRedirect(request, 'Forum/QuestionView.html', {'url': url})
        else:
            form = QuestionForm(instance=question)
    else:
        form = QuestionForm(instance=question)
    return render(
        request, "Forum/QuestionEdit.html", {"form": form, "question": question}
    )


def QuestionDelete(request, ques_id):
    question = Question.objects.get(QuestionID=ques_id)
    question.delete()
    messages.success(request, "Question Deleted")
    return redirect("/forum")


def QuestionView(request, ques_id):
    DisplayQuestion = Question.objects.get(QuestionID=ques_id)
    DisplayAnswers = Answer.objects.filter(question=ques_id)
    liked = False
    for answers in DisplayAnswers:
        total_likes = answers.total_likes()
        liked = False
        if answers.likes.filter(email=request.user.email).exists():
            liked = True
    return render(
        request,
        "Forum/QuestionView.html",
        {
            "DisplayQuestion": DisplayQuestion,
            "DisplayAnswers": DisplayAnswers,
            "answerform": AnswerForm,
            "liked": liked,
        },
    )


def AnswerView(request, ques_id):
    question = get_object_or_404(Question, QuestionID=ques_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            NewAnswer = Answer()
            NewAnswer = form.save(commit=False)
            NewAnswer.question = question
            author = request.user
            NewAnswer.Author = author
            NewAnswer.save()
        return HttpResponseRedirect(
            reverse("Question-view", kwargs={"ques_id": question.QuestionID})
        )
    else:
        form = AnswerForm()
    return render(request, "Forum/AddAnswer.html", {"form": form})


def AnswerEdit(request, ques_id, answer_id):
    question = get_object_or_404(Question, QuestionID=ques_id)
    answer = get_object_or_404(Answer, AnswerID=answer_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("Question-view", kwargs={"ques_id": question.QuestionID})
            )
            # url = reverse(
            #     'Post-view', kwargs={'post_id': post_id, 'comments_id': comments_id})
            # return render(request, 'Dashboard/EditDone.html', {'url': url})
        else:
            form = AnswerForm(instance=answer)
    else:
        form = AnswerForm(instance=answer)
    return render(request, "Forum/AnswerEdit.html", {"form": form, "answer": answer})


def AnswerDelete(request, ques_id, answer_id):
    question = get_object_or_404(Question, QuestionID=ques_id)
    answer = Answer.objects.get(AnswerID=answer_id)
    answer.delete()
    messages.success(request, "Answer Deleted")
    return redirect(f"/forum/{ques_id}")


def LikeView(request, ques_id, answer_id):
    question = get_object_or_404(Question, QuestionID=ques_id)
    answer = get_object_or_404(Answer, AnswerID=answer_id)
    liked = False
    if post.likes.filter(email=request.user.email).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        liked = True
        post.likes.add(request.user)
    return HttpResponseRedirect(
        reverse("Question-view", kwargs={"ques_id": question.QuestionID})
    )


class SearchView(ListView):
    template_name = "Forum/search_question.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q")

        # print(self.request.GET.get("q"))
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            question_results = Question.objects.search(query)
            answer_results = Answer.objects.search(query)

            # combine querysets
            queryset_chain = chain(question_results, answer_results)
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return Question.objects.none()


def LikeView(request, ques_id, answer_id):
    question = get_object_or_404(Question, QuestionID=ques_id)
    answer = get_object_or_404(Answer, AnswerID=answer_id)
    liked = False
    if answer.likes.filter(email=request.user.email).exists():
        answer.likes.remove(request.user)
        liked = False
    else:
        liked = True
        answer.likes.add(request.user)

    return HttpResponseRedirect(
        reverse("Question-view", kwargs={"ques_id": question.QuestionID})
    )


# def search_question(request):
#     if request.method == "POST":
#         searched = request.POST["searched"]
#         return render(request, "Forum/search_question.html", {'searched': searched})
#     else:
#         return render(request, "Forum/search_question.html",)