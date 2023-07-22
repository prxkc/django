from rest_framework import serializers
from .models import Product, Variant, ProductVariantPrice

class ProductVariantPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantPrice
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    product_variant_prices = ProductVariantPriceSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
