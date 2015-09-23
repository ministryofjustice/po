from django.contrib import admin
from django.utils.safestring import mark_safe
from genericadmin.admin import GenericAdminModelAdmin

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


@admin.register(Repository)
class RepositoryAdmin(GenericAdminModelAdmin):
    list_display = ('name',)
    search_fields = ['name', 'description']
    readonly_fields = (
        repo_link, 'private', 'description', 'created', 'updated',
        'contributors', languages, dependencies)
