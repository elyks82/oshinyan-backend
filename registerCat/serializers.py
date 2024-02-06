from rest_framework import serializers
from .models import Recommend, Character, FavoriteThing, CatImage, CatImageByAdmin, Cat, Comment, CommentImage
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = "__all__"

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"
   
class FavoriteThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteThing
        fields = "__all__"

class CatImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatImage
        fields = "__all__"
    
def validate_image_dimensions(image):
        max_width = 800  # specify your maximum width
        max_height = 600  # specify your maximum height
        img = Image.open(image)
        width, height = img.size
        if width > max_width or height > max_height:
            raise serializers.ValidationError('Image width or height exceeds the maximum allowed dimensions.')
        return image

class CatImageByAdminSerializer(serializers.ModelSerializer):
    imgs = serializers.ImageField(validators=[validate_image_dimensions])
    class Meta:
        model = CatImageByAdmin
        fields = "__all__"

class CatSerializer(serializers.ModelSerializer):
    cat_images = CatImageSerializer(read_only=True, many=True)
    cat_admin_images = CatImageByAdminSerializer(read_only=True, many=True)
    recommend = RecommendSerializer(read_only=True, many=True)
    character = CharacterSerializer(many=True, read_only=True)
    favorite_things = FavoriteThingSerializer(many=True, read_only=True)
    class Meta:
        model = Cat
        fields = "__all__"
        depth = 1
    def validate(self, data):
        email = data.get('email')
        if Cat.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'message': 'Email Address already exists'})
        return data

class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    comment_images = CommentImageSerializer(read_only=True, many=True)
    class Meta:
        model = Comment
        exclude = ['cat']
        depth = 2