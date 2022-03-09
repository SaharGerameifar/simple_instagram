from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms 
from django.utils.text import slugify
from django.contrib import messages
from .models import Post, Comment, Like
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from account.models import Relation

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        relation = Relation.objects.filter(from_user=request.user)
        users = []
        for rel in relation:
            users.append(rel.to_user)
        context = {
            'users': users
        }
        return render(request, 'home/index.html', context)


class PostCreateView(LoginRequiredMixin, View):
    form_class = forms.PostCreateUpdateForm

    def get(self , request, *args, **kwargs):
        form = self.form_class
        return render(request,'home/post_create.html',{'form': form,})

    def post(self , request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES) 
        if form.is_valid():
            new_post = form.save(commit=False)  
            new_post.slug = slugify(form.cleaned_data['caption'][:20])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'you created a new post', 'success')
            return redirect('account:user_profile', request.user.id)
        return render(request, 'home/post_create.html', {'form': form,})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully', 'success')
        else:
            messages.error(request, "You can't delete this post", 'danger')
        return redirect('account:user_profile', request.user.id)    


class PostUpdateView(LoginRequiredMixin, View):
    form_class = forms.PostCreateUpdateForm

    def setup(self , request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self , request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "You can't edited this post.", 'danger')
            return redirect('account:user_profile', request.user.id)
        return super().dispatch(request, *args, **kwargs)    

    def get(self , request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        context = {
            'post': post,
            'form':form,
        }
        return render(request,'home/post_update.html', context)

    def post(self , request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.slug = slugify(form.cleaned_data['caption'][:20])
            edited_post.save()
            messages.success(request, 'You edited this post', 'success')
            return redirect('account:user_profile', request.user.id)
        return render(request, 'home/post_update.html', {'form': form,})


class PostDetaileView(View):
    form_class = forms.CommentCreateForm
    form_class_reply = forms.CommentReplyForm

    def setup(self , request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class
        form_reply = self.form_class_reply
        comments = post.postcomments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and post.user_can_like(request.user):
            can_like = True
        context = {
            'post': post,
            'comments': comments,
            'form': form,
            'form_reply': form_reply,
            'can_like': can_like,
        }
        return render(request,'home/post_detail.html',context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
           new_comment = form.save(commit=False)
           new_comment.user = request.user
           new_comment.post = self.post_instance
           new_comment.save()
           messages.success(request, 'Your comment submitted successfully', 'success')
           return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)
        return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class CreateReplyCommentView(LoginRequiredMixin , View):
    form_class = forms.CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.post = post
            reply_comment.reply = comment
            reply_comment.is_reply = True
            reply_comment.save()
            messages.success(request, 'Your reply submitted successfully', 'success')
        return redirect('home:post_detail', post.id, post.slug)


class PostLikeView(LoginRequiredMixin , View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Like.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            messages.success(request, 'You Unliked this post', 'success')
        else:
            Like.objects.create(user=request.user, post=post) 
            messages.success(request, 'You liked this post', 'success')
        return redirect('home:post_detail', post.id, post.slug)       




        