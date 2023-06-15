from django.contrib import admin
from .models import Event, EventAttender

# Register your models here.
admin.site.register(Event)
admin.site.register(EventAttender)