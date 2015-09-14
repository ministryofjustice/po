from distutils.version import StrictVersion

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

        version = obj.__dict__[self.field.name]
        if version is not None:
            if isinstance(version, basestring):
                return StrictVersion(version)

    def __set__(self, obj, value):

        if isinstance(value, basestring) and len(value):
            value = StrictVersion(value)

        if isinstance(value, StrictVersion):
            obj.__dict__[self.field.name] = str(value)
            for name, val in zip(['major', 'minor', 'patch'], list(value.version)):
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
        if isinstance(value, StrictVersion):
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
    name = models.CharField(max_length=30, unique=True)
    version = VersionField()
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
