from django.contrib import admin

from parentApi.models import ParentDataCollection

# Register your models here.
# Register your models here.
@admin.register(ParentDataCollection)
class ParentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone", "address"]
