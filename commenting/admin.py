from django.utils import timezone

from django.contrib import admin

# Register your models here.
from commenting.models import ProductComment
from product.models import ProductBookMark, ProductRating


class ApprovedFilter(admin.SimpleListFilter):
    title = 'approved'
    parameter_name = 'approved'

    def lookups(self, request, model_admin):
        return (
            ('approved', 'approved'),
            ('not-approved', 'not-approved')
        )

    def queryset(self, request, queryset):
        if self.value() == 'approved':
            return queryset.filter(approved_by__isnull=False)
        if self.value() == 'not-approved':
            return queryset.filter(approved_by__isnull=True)


@admin.register(ProductComment)
class commentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'created_time', 'is_approved',]
    list_filter = [ApprovedFilter, ]
    actions = ['set_approved', 'set_disapproved']

    def set_approved(self, request, queryset):
        queryset.filter(approved_by__isnull=True).update(approved_by=request.user, approved_time=timezone.now())

    def set_disapproved(self, request, queryset):
        queryset.filter(approved_by__isnull=False).update(approved_by=None)

admin.site.register(ProductBookMark)
admin.site.register(ProductRating)