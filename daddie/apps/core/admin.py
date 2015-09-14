from distutils.versionpredicate import VersionPredicate
import re

from django.contrib import admin
from django.db.models import Min
from django.utils.safestring import mark_safe

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


def update(obj):
    if isinstance(obj, Deployment):
        priority = obj.build.dependencies.all().aggregate(
            Min('alerts__category__priority'))
        priority = priority['alerts__category__priority__min']
    elif isinstance(obj, Package):
        priority = obj.alerts.all().aggregate(
            Min('category__priority'))
        priority = priority['category__priority__min']
    else:
        priority = obj.dependencies.all().aggregate(
            Min('alerts__category__priority'))
        priority = priority['alerts__category__priority__min']
    img = '<img src="{src}" width="20" height="20" alt="{alt}">'
    if priority is None:
        img = ''
    elif priority < 1:
        img = img.format(
            src='/static/core/admin/img/software-update-urgent.svg',
            alt="Urgent")
    elif priority:
        img = img.format(
            src='/static/core/admin/img/software-update-available.svg',
            alt="Available")
    return mark_safe(img)


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created', update)
    readonly_fields = ('name', 'product', 'created', 'dependencies')


@admin.register(AlertType)
class AlertTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ('environment', 'product', 'created', update)


# package version query syntax
# <query> ::= <pkg-name> <predicate>
# <pkg-name> = ([a-z_]\w*(?:\.[a-z_]\w*)*)
# <predicate> ::= <operator> <version> | <operator> <version> "," <predicate>
# <operator> = "<=" | ">=" | "<" | ">" | "!=" | "=="
# <version> = <text>
re_query = re.compile(
    r'(?i)^\s*([a-z_]\w*(?:\.[a-z_]\w*)*)\s*(<=|>=|<|>|!=|==)\s*(.*)')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'version', 'source']
    list_display = ('name', 'version', 'source', update)
    readonly_fields = ('name', 'version', 'source')
    fields = ('name', 'version', 'source')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PackageAdmin, self).get_search_results(
            request, queryset, search_term)

        query = search_term.strip()
        if not query:
            return queryset, use_distinct

        match = re_query.match(query)
        if not match:
            return queryset, use_distinct

        name, operator, version = match.groups()
        operators = {
            '<': '__lt',
            '<=': '__lte',
            '>': '__gt',
            '>=': '__gte',
            '==': ''}
        if operator in operators:
            kwargs = {'name': name}
            key = 'version{op}'.format(op=operators[operator])
            kwargs.update({key: version})
            queryset |= Package.objects.filter(**kwargs)
        elif operator == '!=':
            queryset |= Package.objects.exclude(version=version)
        else:
            queryset |= Package.objects.filter(name=name)

        return queryset, use_distinct
