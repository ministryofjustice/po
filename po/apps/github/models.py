from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Sum

from core.models import Dependency, Product, Package


class Repository(models.Model):
    name = models.CharField(max_length=100, editable=False, unique=True)
    products = models.ManyToManyField(Product)
    dependencies = GenericRelation(Dependency)
    created = models.DateTimeField(editable=False)
    description = models.TextField(default='', blank=True, null=True)
    updated = models.DateTimeField(editable=False, null=True)
    private = models.BooleanField(default=False)
    url = models.CharField(max_length=255, editable=False)
    contributors = models.IntegerField(editable=False, default=1)
    has_tests = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'repositories'

    def add_language_usages(self, usages):
        for language, num_bytes in usages:
            self.add_language_usage(language, num_bytes)

    def add_language_usage(self, language, num_bytes):
        usage = LanguageUsage()
        usage.language = language
        usage.num_bytes = num_bytes
        self.languages.add(usage)

    def languages_by_usage(self):
        return self.languages.all().values('name', flat=True).order_by(
            '-num_bytes')

    def add_dependency(self, pkg_name, version, source):
        # XXX get a version object because string comparison is buggy
        ver = Package(version=version).version
        package, created = Package.objects.get_or_create(
            name=pkg_name, version=ver, source=source)
        if created:
            package.save()
        dep = Dependency()
        dep.package = package
        dep.dependant = self
        dep.save()


class LanguageUsage(models.Model):
    repository = models.ForeignKey(Repository, related_name='languages')
    language = models.CharField(max_length=30)
    num_bytes = models.IntegerField()

    class Meta:
        unique_together = ('repository', 'language')

    def percentage(self):
        all_langs = LanguageUsage.objects.filter(repository=self.repository)
        total = all_langs.aggregate(Sum('num_bytes'))
        return (float(self.num_bytes) / float(total['num_bytes__sum'])) * 100.0
