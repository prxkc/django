from django.views import generic
from django.db.models import Prefetch
from django.views.generic import ListView
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from rest_framework import generics
from product.serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductListView(ListView):
    template_name = 'products/list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        product_name = self.request.GET.get('product_name')
        product_variant = self.request.GET.get('product_variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        if product_name:
            queryset = queryset.filter(title__icontains=product_name)

        if product_variant:
            queryset = queryset.filter(productvariant__variant_title__icontains=product_variant)

        if price_from and price_to:
            queryset = queryset.filter(productvariant__price__range=(price_from, price_to))

        if date:
            queryset = queryset.filter(created_at=date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()

        # Group variants and options using a dictionary
        variant_options = {}
        variants = Variant.objects.filter(active=True).prefetch_related(
            Prefetch('productvariant_set', queryset=ProductVariant.objects.select_related('variant').order_by('variant_title'))
        ).order_by('title')

        for variant in variants:
            variant_type = variant.title
            variant_options[variant_type] = set([item.variant_title for item in variant.productvariant_set.all()])

        context['variant_options'] = variant_options

        return context