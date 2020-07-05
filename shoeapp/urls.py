from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('showusers/', views.showuser, name='showuser'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('<int:prd_id>/productremove/',views.removeproduct, name='removeproduct'),
    path('<int:user_id>/removeuser/', views.removeuser, name='removeuser'),
    path('showcart/', views.showcart, name='showcart'),
    path('<int:prd_id>/mycart', views.mycart, name='mycart'),
    path('<int:cart_id>/removecart', views.removecart, name='removecart'),
    path('booking/', views.viewbooking, name='booking'),
    path('addbooking/', views.getbookingdata, name='addbooking'),
    path('tracker/', views.tracker, name='tracker'),
    path('viewbymen/', views.viewbymen, name='viewbymen'),
    path('viewbywomen/', views.viewbywomen, name='viewbywomen'),
    path('<int:prdid>updateproduct/', views.updateproduct, name='updateproduct'),
    path('updatebookingstatus/', views.updatebookingstatus, name='updatebookingstatus')
]