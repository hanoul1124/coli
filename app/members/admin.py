from django.contrib import admin

# Register your models here.
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username']

    def save_model(self, request, obj, form, change):
        if change:
            original_obj = User.objects.get(pk=obj.pk)
            if obj.password != original_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(User, UserAdmin)