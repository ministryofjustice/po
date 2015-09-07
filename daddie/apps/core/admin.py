from django.contrib import admin
from django.db.models import Min

from models import Service, Product, Build, AlertType, Deployment, Package,\
    Alert


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'contact_email')


def service_name(obj):
    return obj.service.name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_form_template = 'admin/product_form.html'
    list_display = ('name', service_name)


def priority_alert(obj):
    priority = obj.dependencies.all().aggregate(
        Min('alerts__category__priority'))
    return priority.values()[0]


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('name', priority_alert)
    readonly_fields = ('name', 'product', 'created', 'dependencies')


@admin.register(AlertType)
class AlertTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass
