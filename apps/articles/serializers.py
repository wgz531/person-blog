from rest_framework import serializers
from .models import Articles,ArticlesCategory,Comment
from apps.blogauth.serializers import UserSerializer

class ArticlesCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesCategory
        fields = ('id','name')

class ArticlesSerializer(serializers.ModelSerializer):
    category = ArticlesCategorySerializer()
    author = UserSerializer()
    class Meta:
        model = Articles
        fields = ('id','title','desc','pub_time','category','author')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')