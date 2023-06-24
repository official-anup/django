from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view 
from .forms import ChangePassword, LoginForm,MyPasswordResetForm,MyPasswordResetConfirm
from django.contrib.auth.views import LoginView
urlpatterns = [
    
    path("", views.HomeView.as_view(), name="home"),
    
    path('product-detail/<int:pk>', views.product_detail.as_view(), name='product-detail'),
    
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    path('show-cart/', views.show_cart, name='show-cart'),
    
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removeitem/', views.remove_item),
    
    
    
    
    path('buy/', views.buy_now, name='buy-now'),
    
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('address/', views.address, name='address'),
    
    path('orders/', views.orders, name='orders'),
    path('cancle_orders/', views.cancle_orders, name='cancle_orders'),
    
    
    # path('changepassword/', views.change_password, name='changepassword'),
    
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    
    path('accounts/login/', auth_view.LoginView.as_view(template_name="app/login.html",authentication_form=LoginForm),name="login"),
    
    path('logout/',auth_view.LogoutView.as_view(next_page="login"),name="logout"),
    
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name="app/passwordchange.html",form_class=ChangePassword,success_url="/passwordchangedone/"),name="passwordchange"),
     
    path('passwordchangedone/',auth_view.PasswordChangeView.as_view(template_name="app/passwordchangedone.html"),name="passwordchangedone"),
     
    # path('password-reset/',auth_view.PasswordResetView.as_view(template_name="app/passwordchangedone.html"),name="passwordchangedone"),
    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationForm.as_view(),name="customerregistration"),

    path("password-reset/",auth_view.PasswordResetView.as_view(template_name="app/password_reset.html",form_class=MyPasswordResetForm),name="password_reset"),
    
    path("password-reset/done/",auth_view.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"),name="password_reset_done"),
    
    path("password-reset-confirm/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html",form_class=MyPasswordResetConfirm),name="password_reset_confirm"),
    
    path("password-reset-complete/",auth_view.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"),name="password_reset_complete"),
    
    path('checkout/', views.checkout, name='checkout'),
    
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
