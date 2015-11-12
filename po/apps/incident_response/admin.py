from django.contrib import admin

from core.admin import ProductAdmin
from models import IratStatus


class IratStatusInline(admin.TabularInline):
    model = IratStatus


ProductAdmin.inlines = [IratStatusInline]
