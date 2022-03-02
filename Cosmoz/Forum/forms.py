from Forum.models import Question, Answer
from django.forms import ModelForm
from django import forms
from froala_editor.widgets import FroalaEditor
from django.db.models import Q


class QuestionForm(ModelForm):
    # Image = forms.ImageField()
    Question = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Ask your Question"})
    )

    # Description = forms.CharField(
    #     widget=FroalaEditor, label="Add a description to further explain your question")

    class Meta:
        model = Question
        fields = ("Question",)


class AnswerForm(ModelForm):
    Answer = forms.CharField(widget=FroalaEditor, label="")

    class Meta:
        model = Answer
        fields = ("Answer", "Image")


# class CommentsForm(ModelForm):
#     Comments = forms.CharField(widget=FroalaEditor, label="")

#     class Meta:
#         model = Comments
#         fields = ('Comments',)
