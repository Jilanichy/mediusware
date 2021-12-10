from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView

from django.db.models import Q
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.shortcuts import render, redirect
from django.core.paginator import Paginator


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


# class ProductView(CreateProductView):
#     template_name = 'products/list.html'
#     paginate_by = 10

#     def get_queryset(self):
#         product = Product.objects.all()
#         return product

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product'] = ''
#         context['request'] = ''
#         if self.request.GET:
#             context['request'] = self.request.GET['title__icontains']
#         return context
def product_view(request):
    product = Product.objects.all()
    variants = ProductVariant.objects.all()
    product_info = ProductVariantPrice.objects.all()
    total_product = len(product)
    paginator = Paginator(product_info, 2) # Show 2 product details per page.
    page_number = request.GET.get('page')
    product_info_obj = paginator.get_page(page_number)
    context = {
        'product': product, 'variants': variants, 'product_info': product_info, 'total_product': total_product, 'product_info_obj': product_info_obj
    }

    return render(request, "products/list.html", context)


def search_view(request):
    if request.method == "POST":
        title_search = request.POST["product_title"]
        variant_search = request.POST["variant_search"]
        price_from = request.POST["price_from"]
        price_to = request.POST["price_to"]
        variants = ProductVariant.objects.all()
        product_info = ProductVariantPrice.objects.filter(
              Q(product__title__contains=title_search)
            | Q(product_variant_one__variant_title__contains=variant_search)
            | Q(price__range=[price_from, price_to])
            )

        # total_product = len(product_info)
        # paginator = Paginator(product_info, 1)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
    context = {
        'product_info': product_info, 'variants': variants
    }

    return render(request, "products/product_search.html", context)
