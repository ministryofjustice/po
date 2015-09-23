from distutils.version import LooseVersion, StrictVersion

from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
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


class VersionField(models.Field):
    description = "A version number/string"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super(VersionField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(VersionField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def db_type(self, connection):
        return 'varchar(20)'

    def contribute_to_class(self, cls, name):
        for field_name in ['{0}_major', '{0}_minor', '{0}_patch']:
            field = models.IntegerField(editable=False, null=True, blank=True)
            field.creation_counter = self.creation_counter
            cls.add_to_class(field_name.format(name), field)

        super(VersionField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, VersionCreator(self))

    def get_db_prep_save(self, value, connection):
        if isinstance(value, StrictVersion) or isinstance(value, LooseVersion):
            value = str(value)
        return super(VersionField, self).get_db_prep_save(value, connection)

    def get_db_prep_lookup(self, lookup_type, value, connection, **kwargs):
        if lookup_type == 'exact':
            return [self.get_db_prep_save(value, connection)]

        if lookup_type == 'in':
            return [self.get_db_prep_save(v) for v in value]

        return super(VersionField, self).get_db_prep_lookup(
            lookup_type, value, connection, **kwargs)


class Package(models.Model):
    name = models.CharField(max_length=30)
    version = VersionField()
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
