from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class ApprovedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(approved_by__isnull=False)


class ProductComment(models.Model):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self._vote_results = None

    created_time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments_user')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name='comments_approved_users', editable=False)
    approved_time = models.DateTimeField(blank=True, null=True, editable=False)
    content = models.TextField()
    objects = models.Manager()
    approves = ApprovedManager()

    def is_approved(self):
        return bool(self.approved_by)

    is_approved.boolean = True

    def vote_results(self):
        if self._vote_results is None:
            self._vote_results = self.votes.aggregate(
                positive_votes=Coalesce(
                    models.Sum(
                        models.Case(
                            models.When(vote__gt=0, then='vote')
                        )
                    ), 0
                ),
                negative_votes=Coalesce(
                    models.Sum(
                        models.Case(
                            models.When(vote__lt=0, then='vote')
                        )
                    ), 0
                ),
            )

        return self._vote_results

    def positive_votes(self):
        return self.vote_results()['positive_votes']

    def negative_votes(self):
        return abs(self.vote_results()['negative_votes'])


class CommentVote(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_("user"), related_name='votes')
    comment = models.ForeignKey('ProductComment', on_delete=models.CASCADE, verbose_name=_("comment"),
                                related_name='votes')
    vote = models.SmallIntegerField(_('vote'), validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_vote')
        ]
        verbose_name_plural = _("Comment votes")
        verbose_name = _("Comment vote")
