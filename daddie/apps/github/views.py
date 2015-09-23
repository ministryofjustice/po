from rest_framework import permissions, viewsets

import models
import serializers


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = models.Repository.objects.all()
    serializer_class = serializers.RepositorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
