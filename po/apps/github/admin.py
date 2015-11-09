from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.utils.safestring import mark_safe

from models import Repository


def languages(obj):
    return mark_safe(
        '<div style="float:left">' +
        ''.join(
            '<li>{language} - {percentage:.1f}%</li>'.format(
                language=l.language,
                percentage=l.percentage())
            for l in obj.languages.all().order_by('-num_bytes')) +
        '</div>')


def dependencies(obj):
    return u', '.join(map(unicode, obj.dependencies.all()))


def repo_link(obj):
    return mark_safe('<a href="{0.url}">{0.name}</a>'.format(obj))


def add_to_product(modeladmin, request, queryset):
    return HttpResponseRedirect(
        '/admin/add-repo-to-product/?repo_ids={ids}'.format(
            ids=','.join(request.POST.getlist(admin.ACTION_CHECKBOX_NAME))))


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    actions = [add_to_product]
    list_display = ('name',)
    search_fields = ['name', 'description']
    readonly_fields = (
        repo_link, 'private', 'description', 'created', 'updated', 'has_tests',
        'contributors', languages, dependencies)
