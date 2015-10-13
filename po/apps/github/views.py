from django.views.generic.edit import FormView
from django.contrib import messages
from rest_framework import permissions, viewsets

import forms
import models
import serializers


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = models.Repository.objects.all()
    serializer_class = serializers.RepositorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AddRepoToProductFormView(FormView):
    template_name = 'admin/add_repo_to_product_form.html'
    form_class = forms.AddRepoToProductForm
    success_url = '/admin/github/repository/'

    def get_context_data(self, **kwargs):
        context = super(
            AddRepoToProductFormView, self).get_context_data(**kwargs)
        context['opts'] = models.Repository._meta
        context['app_label'] = models.Repository._meta.app_label
        return context

    def form_valid(self, form):
        repos = models.Repository.objects.filter(
            pk__in=self.request.GET['repo_ids'].split(','))
        product = models.Product.objects.get(
            pk=form.cleaned_data['product_id'])
        repos.products.add(product)
        repos.save()
        messages.success(self.request, 'Added {repos} to {product}'.format(
            repos=', '.join(map(lambda r: r.name, repos)),
            product=product.name))
        return super(AddRepoToProductFormView, self).form_valid(form)
