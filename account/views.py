from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from home.models import Post
from .models import Relation,Profile
from django.http import Http404

class UserRegisterView(View):
    form_class = forms.UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context ={
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            User.objects.create_user(clean_data['username'], clean_data['email'], clean_data['password1'])
            messages.success(request,'You registered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form,})


class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context ={
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request, username=clean_data['username'], password=clean_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request,'You login successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')    
            messages.error(request,'Username/Email or Password is wrong', 'danger')
        return render(request, self.template_name, {'form': form,})


class UserLogoutView(LoginRequiredMixin, View):
        
    def get(self, request):
        logout(request)
        messages.success(request,'You logout successfully', 'success')
        return redirect('home:home')    
    

class UserPasswordRestView(auth_views.PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    success_url = reverse_lazy('account:user_password_reset_done') 


class UserPasswordRestDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordRestConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:user_password_reset_complete')


class UserPasswordRestCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserEditProfileView(LoginRequiredMixin, View):
    form_class = forms.EditUserProfile


    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email':request.user.email, 'first_name':request.user.first_name, 'last_name':request.user.last_name})
        context = {
            'form': form,
        }
        return render(request, 'account/edit_profile.html', context)


    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            messages.success(request, 'profile edited successfully', 'success')
        return redirect('account:edit_user_profile')


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        is_following = False
        following = 0 
        followers = 0
        count_post = 0
        user = get_object_or_404(User, pk=user_id)
        posts = user.userpostes.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True

        context = {
            'user': user,
            'posts': posts,
            'is_following': is_following,
            'following': Profile.followers_count(user),
            'followers': Profile.followings_count(user),
            'count_post': Profile.posts_count(user),
        }
        
        return render(request,'account/profile.html',context)


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user) 
        if relation.exists():
            messages.error(request,'you are already following this user','danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request,'you followed this user','success')
        return redirect('account:user_profile', user.id)    


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user) 
        if relation.exists():
            relation.delete()
            messages.success(request,'you unfollowed this user','success')
        else:
            messages.error(request,'you are not following this user','danger')
        return redirect('account:user_profile', user.id) 


class UserFollowerView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(to_user=user) 
        if relation.exists():
            context = {
                'user': user,
                'relation': relation,
            }
            return render(request,'account/user_follower_list.html',context)
        else:
            messages.error(request,'This user not follower yet','danger')
        return redirect('account:user_profile', user.id) 


class UserFollowingView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=user) 
        if relation.exists():
            context = {
                'user': user,
                'relation': relation,
            }
            return render(request,'account/user_following_list.html',context)
        else:
            messages.error(request,'This user not following yet','danger')
        return redirect('account:user_profile', user.id)   


class SearchUserView(View):
    def get(self, request):
        search = request.GET.get('search')
        users = User.objects.filter(username__icontains=request.GET['search'])
        if users is not None and search:
            return render(request, 'account/search_user.html',{ 'users': users, })
        raise Http404('This field is empty. Please enter a username')       
                  