from django.shortcuts import render

from po.apps.core.admin import search_query
from po.apps.core.models import Build, Package, Product, Dependency
from po.apps.github.models import Repository


def product_query_form(request):
    if 'q' in request.GET:
        packages = Package.objects.filter(name='')
        packages = list(search_query(request.GET['q'].strip(), packages))
        pkg_ids = [pkg.id for pkg in packages]
        dependencies = Dependency.objects.filter(
            package__in=pkg_ids)
        products = Product.objects.filter(
            )

        results = list(products)

        # def dependencies(product):
            # deps = []

                # pk__in=product.builds.filter(dependencies__package.values('pk'))
            # deps |= packages.filter(
                # pk__in=product.repositories.all().dependencies.all().values('pk'))
            # return deps

        # results = zip(products, map(dependencies, products))

        return render(request, 'admin/product_query_results.html', {
            'results': results, 'query': request.GET['q'].strip()})
    return render(request, 'admin/product_query_form.html')
