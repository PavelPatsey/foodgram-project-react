from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="subscribers",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор на которого подписались",
        related_name="subscribed_authors",
    )

    class Meta:
        unique_together = (
            "user",
            "author",
        )
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_user_author_subscription",
            )
        ]

    def __str__(self):
        return f"{self.user}_to_{self.author}"
