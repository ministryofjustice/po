from django.shortcuts import render

from po.apps.core.admin import search_query
from po.apps.core.models import Package, Product


def product_query_form(request):
    if 'q' in request.GET:
        packages = Package.objects.filter(name='')
        packages = search_query(request.GET['q'].strip(), packages)
        pkg_ids = packages.values('pk')

        products = Product.objects.filter(
            builds__dependencies__package__in=pkg_ids)
        products |= Product.objects.filter(
            repository__dependencies__package__in=pkg_ids)

        return render(request, 'admin/product_query_results.html', {
            'results': products, 'query': request.GET['q'].strip()})
    return render(request, 'admin/product_query_form.html')
