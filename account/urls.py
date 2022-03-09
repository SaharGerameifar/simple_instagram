from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('password/reset/', views.UserPasswordRestView.as_view(), name='user_password_reset'),
    path('password/reset/done/', views.UserPasswordRestDoneView.as_view(), name='user_password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordRestConfirmView.as_view(), name='user_password_reset_confirm'),
    path('complete/', views.UserPasswordRestCompleteView.as_view(), name='user_password_reset_complete'),
    path('edite_profile/', views.UserEditProfileView.as_view(), name='edit_user_profile'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnFollowView.as_view(), name='user_unfollow'),
    path('followers/<int:user_id>/', views.UserFollowerView.as_view(), name='user_followers'),
    path('followings/<int:user_id>/', views.UserFollowingView.as_view(), name='user_followings'),
    path('search/', views.SearchUserView.as_view(), name='user_search'),
]
