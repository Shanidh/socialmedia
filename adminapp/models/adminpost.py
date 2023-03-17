from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class PostType(models.TextChoices):
    FOOD = "FOOD", _("Food")
    TRAVEL = "TRAVEL", _("Travel")
    OTHERS = "OTHERS", _("Others")


class Tag(models.Model):
    name = models.CharField(max_length=50)
    weight = models.IntegerField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    like = models.BooleanField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True)

    post_type = models.CharField(
        help_text=_("User Type"),
        max_length=20,
        choices=PostType.choices,
        null=True,
    )

    tags = models.ForeignKey(
        help_text=_("Tag"),
        to=Tag,
        on_delete=models.CASCADE,
        related_name="tags",
        null=True,
    )


class Image(models.Model):
    post = models.ForeignKey(
        help_text=_("Post"),
        to=Post,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.FileField(upload_to='images/')
    description = models.CharField(max_length=100)    