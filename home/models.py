from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

class Post(models.Model):
    def generate_filename(self, filename):
        name = "PostUploads/%s/%s" % (self.user.username, filename)
        return name

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userpostes')
    image = models.ImageField(upload_to=generate_filename)
    caption = models.CharField(max_length=350)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username} - {self.updated}'     

    def image_tag(self):
        return format_html(
            f"<img src={self.image.url} width='100' height='75' style='border-radius:5px;'>")

    image_tag.short_description = "PostImage"

    def comments_count(self):
        return self.postcomments.count()
        
    def user_can_like(self, user):
        user_like = user.userlikes.filter(post=self)
        if user_like.exists():
            return True
        return False
    

   
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postcomments')
    body = models.TextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replycomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'
        
    class Meta:
        ordering = ('-created',)  


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userlikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postlikes')

    def __str__(self):
        return f'{self.user.username} like {self.post.slug}'        
