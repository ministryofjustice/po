from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Sum

from po.apps.core.models import Dependency, Product, Package


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

    class Meta:
        verbose_name_plural = 'repositories'


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
