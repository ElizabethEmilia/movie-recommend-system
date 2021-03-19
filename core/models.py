from django.db import models

# Create your models here.

class Movie(models.Model):

    director = models.CharField(max_length=100, verbose_name='导演')
    score = models.CharField(max_length=100, verbose_name='评分')
    name = models.CharField(max_length=100, verbose_name='名称')
    movietype = models.CharField(max_length=100, verbose_name='类型')
    img = models.CharField(max_length=500, verbose_name='图片', default='')

    class Meta(object):
        verbose_name = verbose_name_plural = '电影表'

    def __str__(self):
        return self.name

class User(models.Model):

    name = models.CharField(max_length=100, verbose_name = '姓名')
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    mobile = models.CharField(max_length=100, verbose_name='手机号')
    interesting = models.CharField(max_length=500, verbose_name='兴趣爱好')

    class Meta(object):
        verbose_name = verbose_name_plural = '用户表'

    def __str__(self):
        return self.username

class MovieUserScore(models.Model):

    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, verbose_name='电影')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户')
    score = models.CharField(max_length=100, verbose_name='分数', default='')

    class Meta(object):
        verbose_name = verbose_name_plural = '用户评分表'


    def __str__(self):
        return self.user.name + '__' + self.movie.name


class MovieUserComment(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, verbose_name='电影')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户')
    comment = models.CharField(max_length=1000, verbose_name='评论')


