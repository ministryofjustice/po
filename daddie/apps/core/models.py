from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=30, unique=True)
    contact_name = models.CharField(max_length=30)
    contact_email = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    service = models.ForeignKey(Service, related_name='products')

    def __unicode__(self):
        return unicode(' / '.join([unicode(self.service), self.name]))


class Package(models.Model):
    name = models.CharField(max_length=30, unique=True)
    major = models.IntegerField(default=0)
    minor = models.IntegerField(default=0)
    patch = models.IntegerField(default=0)
    extra_version = models.CharField(max_length=30)
    source = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode(self.name)


class Build(models.Model):
    name = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, related_name='builds')
    dependencies = models.ManyToManyField(Package, through='Dependency')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(' / '.join([
            unicode(self.product),
            self.name]))


class Dependency(models.Model):
    package = models.ForeignKey(Package, related_name='dependants')
    build = models.ForeignKey(Build)

    class Meta:
        verbose_name_plural = 'dependencies'

    def __unicode__(self):
        return unicode(self.package)


class Deployment(models.Model):
    environment = models.CharField(max_length=30)
    product = models.ForeignKey(Product, related_name='deployments')
    build = models.ForeignKey(Build, related_name='deployments')
    created = models.DateTimeField(auto_now_add=True)


class AlertType(models.Model):
    name = models.CharField(max_length=30)
    priority = models.IntegerField(null=False, default=0)

    def __unicode__(self):
        return unicode(self.name)


class Alert(models.Model):
    package = models.ForeignKey(Package, related_name='alerts')
    category = models.ForeignKey(AlertType, related_name='alerts')

    def __unicode__(self):
        return u'{alert} on {package} [{source}]'.format(
            alert=unicode(self.category),
            package=unicode(self.package),
            source=unicode(self.package.source))
