from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=((0, 'Inactive'),(1, 'Active')))
    type = models.PositiveSmallIntegerField(choices=((1,'Admin'),(2,'User'),(3,'Guest User')))

    def __str__(self):
        return self.name


class Asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,unique=True)
    asset_type = models.PositiveSmallIntegerField(choices=((1,'Movie'),(2,'Documentary'),(3,'Season'),(4,'Episode')))
    video_url = models.TextField(default=None,null=True)
    parent_asset_id = models.IntegerField(default=0,null=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    asset_id = models.ForeignKey(Asset,on_delete=models.CASCADE)
    parent_comment_id = models.IntegerField(default=0,null=True)

    class Meta:
        unique_together = ['uid','asset_id']

    def __str__(self):
        return "{0}-{1}".format(self.asset_id.title,self.comment)


class Like(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    adate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['uid', 'asset_id']


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)])

    class Meta:
        unique_together = ['uid','asset_id']

    def __str__(self):
        return "{0} -{1}/10".format(self.asset_id.title,self.rating)




