from django.urls import path
from . import views

urlpatterns = [
     path('log', views.log),
     path('admin1',views.admin_home),
     path('logout',views.AU_logout),
     path('category',views.add_category),
     path('add_prodect',views.add_product),
     path('delete_category/<int:id>/', views.delete_category, name='delete_category'),

     


     #________user______
     path('register',views.reg),
     path('',views.user_home)
]
