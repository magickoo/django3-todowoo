from django.contrib import admin
from .models import Todo
# Register your models here.


#to show created field
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    
admin.site.register(Todo, TodoAdmin)
