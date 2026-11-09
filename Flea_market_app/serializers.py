# api/serializers.py
from rest_framework import serializers
from .models import Category, Profile, Product, ProductImage, Review, Message, Favorite
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    seller = ProfileSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller', 'views', 'created_at', 'updated_at']

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    # Для загрузки нескольких изображений через multipart/form-data
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'city', 'address', 'condition', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product

class ReviewSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['user']

class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'created_at', 'is_read']