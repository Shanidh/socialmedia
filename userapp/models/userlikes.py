from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from adminapp.models import Post


class LikeStatus(models.TextChoices):
    LIKE = "LIKE", _("Like")
    DISLIKE = "DISLIKE", _("Dislike")


class LikedPosts(models.Model):
    post = models.ForeignKey(
        help_text=_("Like Post"),
        to=Post,
        on_delete=models.CASCADE,
        related_name="likedposts",
    )

    status = models.CharField(
        help_text=_("Like Status"),
        max_length=20,
        choices=LikeStatus.choices,
        null=True,
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likestatususer", null=True
    )
