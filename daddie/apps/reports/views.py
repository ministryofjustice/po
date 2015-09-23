from django.shortcuts import render

from daddie.apps.core.admin import search_query
from daddie.apps.core.models import Package, Product
from daddie.apps.github.models import Repository


def product_query_form(request):
    if 'q' in request.GET:
        packages = Package.objects.filter(name='')
        packages = search_query(request.GET['q'].strip(), packages)
        products = Product.objects.filter(
            builds__dependencies__package__in=packages.values('pk'))
        products |= Product.objects.filter(
            repository__dependencies__package__in=packages.values('pk'))

        return render(request, 'product_query_results.html', {
            'results': products, 'query': request.GET['q'].strip()})
    return render(request, 'product_query_form.html')
