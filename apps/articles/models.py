from django.db import models

class ArticlesCategory(models.Model):
    name = models.CharField(max_length=100)

class Articles(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('ArticlesCategory', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('blogauth.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-pub_time']

class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    articles = models.ForeignKey('Articles',on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('blogauth.User',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']
