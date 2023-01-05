from django.urls import path
from . import views

urlpatterns = [
    path('', views.getUserDetail,name="home"),
    path('bill/<int:id>',views.update_bill,name='update_bill'),
    
    path('transaction',views.createTransaction,name="transaction"),
    path('transaction/<str:pk>',views.update_transaction,name="update_transaction"),
    path('transaction/delete/<str:pk>',views.delete_transaction,name="delete_transaction"),

    path('show',views.show_bill,name='show_bill'),
    path('profile', views.update_profile,name="profile"),
    path('login', views.login_view,name="login"),
    path('logout', views.logout_view,name="logout"),
    path('register', views.register_view,name="register"),
    
]
