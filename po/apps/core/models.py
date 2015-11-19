from distutils.version import LooseVersion, StrictVersion, Version

from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=30, unique=True)
    contact_name = models.CharField(max_length=30)
    contact_email = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True, null=True)
    service = models.ForeignKey(Service, related_name='products', null=True)

    def __unicode__(self):
        return unicode(' / '.join([unicode(self.service), self.name]))


class VersionCreator(object):

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance')

        version = obj.__dict__.get(self.field.name)
        if version is not None:
            if isinstance(version, basestring):
                try:
                    return StrictVersion(version)
                except ValueError:
                    return LooseVersion(version)

    def __set__(self, obj, value):

        if isinstance(value, basestring) and len(value):
            obj.__dict__[self.field.name] = value
            try:
                value = StrictVersion(value)
            except ValueError:
                value = LooseVersion(value)

        subfields = ['major', 'minor', 'patch']

        if isinstance(value, StrictVersion):
            obj.__dict__[self.field.name] = str(value)
            pairs = zip(subfields, list(value.version))
            for name, val in pairs:
                setattr(obj, '{0}_{1}'.format(self.field.name, name), val)

        if isinstance(value, LooseVersion):
            obj.__dict__[self.field.name] = str(value)
            pairs = zip(subfields[:len(value.version)], list(value.version))
            for name, val in pairs:
                setattr(obj, '{0}_{1}'.format(self.field.name, name), val)


def parse_version(value):
    try:
        return StrictVersion(value)
    except ValueError:
        return LooseVersion(value)
    raise exceptions.ValidationError(
        'Invalid input for a Version: %s' % value)


class VersionField(models.CharField):
    description = "A version number/string"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super(VersionField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super(VersionField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return parse_version(value)

    def to_python(self, value):
        if isinstance(value, None):
            return value
        if isinstance(value, Version):
            return value
        if isinstance(value, basestring):
            return parse_version(value)

    def get_prep_value(self, value):
        return str(value)


class Package(models.Model):
    name = models.CharField(max_length=30)
    version = VersionField()
    version_major = models.IntegerField(null=True)
    version_minor = models.IntegerField(null=True)
    version_patch = models.IntegerField(null=True)
    source = models.CharField(max_length=30, null=True)

    class Meta:
        select_on_save = True
        unique_together = ('name', 'version', 'source')

    def __unicode__(self):
        return unicode(self.name)


class Dependency(models.Model):
    package = models.ForeignKey(Package, related_name='dependants')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    dependant = GenericForeignKey()

    class Meta:
        verbose_name_plural = 'dependencies'
        unique_together = ('package', 'content_type', 'object_id')

    def __unicode__(self):
        return u'{0.package}-{0.package.version}'.format(self)


class Build(models.Model):
    name = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, related_name='builds')
    dependencies = GenericRelation(Dependency)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'created')

    def __unicode__(self):
        return unicode(' / '.join([
            unicode(self.product),
            self.name]))


class Deployment(models.Model):
    environment = models.CharField(max_length=30)
    build = models.ForeignKey(Build, related_name='deployments')
    created = models.DateTimeField(auto_now_add=True)
    has_healthcheck_json = models.BooleanField(default=False)
    has_ping_json = models.BooleanField(default=False)

    class Meta:
        unique_together = ('environment', 'build', 'created')


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
