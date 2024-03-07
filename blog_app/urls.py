from django.urls import path
from.import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.login,name="login"),
    path('home/',views.home,name="home"),
    path('signup/',views.signup,name="signup"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('logout/',views.logout,name="logout"),
    path('blogcontent/<int:id>',views.blogcontent,name="blogcontent"),
    path('comment/',views.comment,name="comment"),
    path('reply/',views.reply,name="reply"),


    #reset password urls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]