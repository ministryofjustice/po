from rest_framework import permissions, viewsets, authentication

import models
import serializers


class SessionCsrfExemptAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class ServiceViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionCsrfExemptAuthentication,
        authentication.BasicAuthentication)
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionCsrfExemptAuthentication,
        authentication.BasicAuthentication)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PackageViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionCsrfExemptAuthentication,
        authentication.BasicAuthentication)
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DependencyViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionCsrfExemptAuthentication,
        authentication.BasicAuthentication)
    queryset = models.Dependency.objects.all()
    serializer_class = serializers.DependencySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BuildViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionCsrfExemptAuthentication,
        authentication.BasicAuthentication)
    queryset = models.Build.objects.all()
    serializer_class = serializers.BuildSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DeploymentViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionCsrfExemptAuthentication,
        authentication.BasicAuthentication)
    queryset = models.Deployment.objects.all()
    serializer_class = serializers.DeploymentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
