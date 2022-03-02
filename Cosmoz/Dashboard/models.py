from django.db import models
from Accounts.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
import uuid
from froala_editor.fields import FroalaField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField


# from FroalaEditor.froala_editor import views as froala_views

# Create your models here.


class Post(models.Model):
    def directory(instance, filename):
        DirectoryPath = f"{instance.Author}/Posts/{instance.PostID}.jpg"
        # return str(settings.BASE_DIR.joinpath(DirectoryPath))
        print("From Post ", DirectoryPath)
        return DirectoryPath

    PostID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # RoomID=models.CharField(max_length=20)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Caption = models.CharField(max_length=100)
    TextContent = RichTextField()
    TimeStamp = models.DateTimeField(default=timezone.now)
    # print("From Post ",directory())
    Image = models.ImageField(upload_to=directory)
    likes = models.ManyToManyField(User, related_name="blog_post")

    def total_likes(self):
        return self.likes.count()
    
    

    def _str_(self):
        return self.Title


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    CommentsID = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    TextContent = FroalaField(image_upload=False)
    TimeStamp = models.DateTimeField(default=timezone.now)
    # Image= models.ImageField(upload_to = DirectoryPath(User,post))
    # approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    class meta:
        ordering = "TimeStamp"

    def str(self):
        return f"Comment by {self.Author} on {self.post}"