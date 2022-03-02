from Dashboard.models import Post, Comments
from django.forms import ModelForm
from django import forms
from froala_editor.widgets import FroalaEditor


class PostForm(ModelForm):
    Image = forms.ImageField()
    Title = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Title"})
    )
    Caption = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Caption"})
    )

    TextContent = forms.CharField(widget=FroalaEditor, label="")

    class Meta:
        model = Post
        fields = (
            "Title",
            "Caption",
            "TextContent",
            "Image",
        )

    Caption.widget.attrs["class"] = "form-control"
    Title.widget.attrs["class"] = "form-control"


class CommentForm(ModelForm):
    TextContent = forms.CharField(widget=FroalaEditor, label="")

    class Meta:
        model = Comments
        fields = ("TextContent",)
