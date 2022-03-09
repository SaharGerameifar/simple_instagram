from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput())
    
    class Meta:
        model = Post
        fields = ('image', 'caption')


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)        