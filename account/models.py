from django.db import models
from django.contrib.auth.models import User
from home.models import Post


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length= 250 ,null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatar')

    def followers_count(self):
            return self.followers.count()

    def followings_count(self):
            return self.following.count()        

    def posts_count(self):
            return self.userpostes.count()