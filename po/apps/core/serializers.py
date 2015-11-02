from distutils.version import LooseVersion, StrictVersion, Version
import importlib
import logging
import re

from rest_framework import serializers

import models


log = logging.getLogger(__name__)


# XXX - monkeypatch __cmp__ in *Version classes because they assume that the
# other value is not None
def fix_cmp(fn):
    def cmp_fixed(self, other):
        if other is None:
            # hopefully, nothing is ever version 0.0.0
            other = '0.0.0'
        return fn(self, other)
    return cmp_fixed
LooseVersion.__cmp__ = fix_cmp(LooseVersion.__cmp__)
StrictVersion.__cmp__ = fix_cmp(StrictVersion.__cmp__)


class ServiceSerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='product-detail',
        lookup_field='pk')

    class Meta:
        model = models.Service
        fields = ('name', 'contact_name', 'contact_email', 'products')


class ProductSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(required=False)

    class Meta:
        model = models.Product

    def create(self, validated_data):
        service_data = validated_data.pop('service', None)
        if service_data:
            service, _ = models.Service.objects.get_or_create(**service_data)
            validated_data['service'] = service
        log.debug('product create data: %s' % str(validated_data))
        product, _ = models.Product.objects.get_or_create(**validated_data)
        return product


class VersionField(serializers.Field):

    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        if data is None:
            return data
        if isinstance(data, Version):
            return data
        if isinstance(data, basestring):
            try:
                return StrictVersion(data)
            except ValueError:
                return LooseVersion(data)
            except TypeError:
                raise Exception(data.__class__.__name__)
        raise serializers.ValidationError(
            '%s not recognised as a version string' % data)


class PackageSerializer(serializers.ModelSerializer):
    version = VersionField()

    class Meta:
        model = models.Package
        fields = ('name', 'version', 'source')


def module_path(obj):
    # XXX - hacky
    match = re.match(r"<class '(.*)\.([^.']+)'>", str(type(obj)))
    if match:
        return match.groups()
    return None, None


class DependantObjectRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        module, model = module_path(value)
        log.debug('dependant object: %s' % value)
        return {
            'type': model,
            'pk': value.pk,
            'value': str(value)}


class DependencySerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    dependant = DependantObjectRelatedField(read_only=True)

    class Meta:
        model = models.Dependency
        depth = 0
        fields = ('package', 'dependant',)

    def to_representation(self, obj):
        return unicode(obj)


class BuildSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    dependencies = DependencySerializer(many=True)

    class Meta:
        model = models.Build
        depth = 0
        fields = ('name', 'product', 'dependencies')

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product = ProductSerializer().create(product_data)
        validated_data['product'] = product
        dependency_data = validated_data.pop('dependencies')
        log.debug('build data: %s' % str(validated_data))
        build = models.Build.objects.create(**validated_data)
        for data in dependency_data:
            pkg_data = data['package']
            package = PackageSerializer(data=pkg_data)
            log.debug('package: %s' % str(pkg_data))
            log.debug('is valid? %s' % package.is_valid())
            if package.is_valid():
                package = package.create(pkg_data)
                models.Dependency.objects.create(
                    package=package,
                    dependant=build)
        log.debug('build dependencies: %s' % str(build.dependencies.all()))
        return build


class DeploymentSerializer(serializers.ModelSerializer):
    build = BuildSerializer()

    class Meta:
        model = models.Deployment
        fields = ('environment', 'build')

    def create(self, validated_data):
        build_data = validated_data.pop('build')
        build = BuildSerializer().create(build_data)
        validated_data['build'] = build
        log.debug('deployment data: %s' % str(validated_data))
        deployment = models.Deployment.objects.create(**validated_data)
        return deployment
