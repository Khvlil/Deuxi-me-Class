from django.contrib import admin
from .models import User, UserManager, Reporter, UserSubscription
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joinded')
    list_filter = ("is_confirmed", )
    search_fields = ('username', 'email')


class ReporterAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'subject', 'date_writing')
    search_fields = ('reporter',)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'subscribed', 'free_trial',
                    'free_trial_expired', 'subscription_expired',)
    search_fields = ('client',)


admin.site.register(User, UserAdmin)
admin.site.register(Reporter, ReporterAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
