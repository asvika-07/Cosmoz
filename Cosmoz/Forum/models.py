from django.db import models
from Accounts.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
import uuid
from froala_editor.fields import FroalaField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField
from django.db.models import Q


class QuestionManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(Question__icontains=query))
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class AnswerManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(Answer__icontains=query))
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs

class Question(models.Model):
    QuestionID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # RoomID=models.CharField(max_length=20)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Question = models.CharField(max_length=300)
    Description = RichTextField(null=True, blank=True)
    TimeStamp = models.DateTimeField(default=timezone.now)
    Image = models.ImageField(null=True, blank=True)

    objects = QuestionManager()

    class meta:
        ordering = "TimeStamp"

    def __str__(self):
        return str(self.QuestionID)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answer"
    )
    AnswerID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # RoomID=models.CharField(max_length=20)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)

    Answer = RichTextField(null=True, blank=True)
    TimeStamp = models.DateTimeField(default=timezone.now)
    Image = models.ImageField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="AnswerLikes")

    objects = AnswerManager()

    # objects = ForumManager()

    def total_likes(self):
        return self.likes.count()

    class meta:
        ordering = "TimeStamp"

    def __str__(self):
        return str(self.AnswerID)

