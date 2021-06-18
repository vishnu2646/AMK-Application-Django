from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="signin"),
    path('adminlogin/',views.adminlogin,name="admin-signin"),
    path('home/',views.index,name="home"),
    path('prices/',views.pricelist,name="prices"),
    path('orders/',views.products,name="orders"),
    path('order/<int:pk>/edit/',views.deliveryupdate,name="order-edit"),
    path('delivery/',views.delevery,name="delivery"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.register,name="signup"),
    # checking
    path('bill/',views.caluclation,name="calc"),
    path('payment/',views.payment,name="pay"),
    path('success/',views.payment_status,name="payment-success"),
]