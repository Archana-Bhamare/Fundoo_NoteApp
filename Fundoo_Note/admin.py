from django.contrib import admin

# Register your models here.
from Fundoo_Note.models import *

admin.site.register(Notes)
admin.site.register(Label)