from rest_framework import serializers

import models


class RepositorySerializer(serializers.ModelSerializer):
    # dependencies = serializers.HyperlinkedRelatedField(
        # many=True,
        # read_only=True,
        # view_name='dependency-detail')

    class Meta:
        model = models.Repository
        fields = (
            'name', 'products', 'created', 'description',
            'updated', 'private', 'url')

