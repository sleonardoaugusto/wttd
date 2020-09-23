from django.contrib import admin

from eventex.subscriptions.models import Subscription


class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cpf",
        "email",
        "phone",
        "created_at",
    )
    date_hierarchy = "created_at"


admin.site.register(Subscription, SubscriptionModelAdmin)
