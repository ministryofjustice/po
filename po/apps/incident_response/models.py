from django.db import models

from core.models import Product


class IratStatus(models.Model):
    product = models.OneToOneField(Product)
    incidents_in_last_two_weeks = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'IRAT Status'
        verbose_name_plural = 'IRAT Status'

    def __unicode__(self):
        return u'Incidents for {product} in the last 2 weeks: {count}'.format(
            product=self.product.name,
            count=self.incidents_in_last_two_weeks)
