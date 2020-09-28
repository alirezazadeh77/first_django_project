from django.db import models
from django.conf import settings


# Create your models here.

class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approved_by__isnull=False)


class ProductComment(models.Model):
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
