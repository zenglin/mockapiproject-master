from django.contrib import admin
from .models import *

class CaseidAdmin(admin.ModelAdmin):
    pass

admin.site.register(CaseidMock, CaseidAdmin)
