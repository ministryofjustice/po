import importlib
import logging
import re

from rest_framework import serializers

import models


log = logging.getLogger(__name__)


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
    service = ServiceSerializer()

    class Meta:
        model = models.Product

    def create(self, validated_data):
        service_data = validated_data.pop('service')
        log.debug(service_data)
        service, _ = models.Service.objects.get_or_create(**service_data)
        validated_data['service'] = service
        product, _ = models.Product.objects.get_or_create(**validated_data)
        return product


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = ('name', 'version', 'source')


def module_path(obj):
    # XXX - hacky
    match = re.match(r"<class '(.*)\.([^.']+)'>", str(type(obj)))
    if match:
        return match.groups()
    return None, None


def parent_module(path):
    return path.rpartition('.')[0]


def serializer_for(obj):
    module, model = module_path(obj)
    if module and model:
        module = '{module}.serializers'.format(module=parent_module(module))
        serializer = '{model}Serializer'.format(model=model)
        try:
            module = importlib.import_module(module)
            serializer_class = getattr(module, serializer)
            return serializer_class(obj)
        except ImportError:
            pass
    raise ValueError('Could not find serializer for {0}'.format(model))


class DependantObjectRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, models.Build):
            data = BuildSerializer(value).data
            data.update({'type': 'Build'})
        else:
            module, model = module_path(value)
            data = serializer_for(value).data
            data.update({'type': model})

        return data


class DependencySerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    dependant = DependantObjectRelatedField(read_only=True)

    class Meta:
        model = models.Dependency
        fields = ('package', 'dependant',)


class BuildSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    dependencies = DependencySerializer(many=True)

    class Meta:
        model = models.Build
        fields = ('name', 'product', 'dependencies')

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product = ProductSerializer().create(product_data)
        validated_data['product'] = product
        dependency_data = validated_data.pop('dependencies')
        build = models.Build.objects.create(**validated_data)
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
        log.debug('deployment', validated_data)
        deployment = models.Deployment.objects.create(**validated_data)
        return deployment
