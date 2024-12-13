from django.urls import path
from . import views

urlpatterns = [
     path('log', views.log),
     path('admin1',views.admin_home),
     path('logout',views.AU_logout),
     path('category',views.add_category),
     path('add_prodect',views.add_products),
     path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
     path('viewproduct',views.view_pro),
     path('deletepro/<pid>',views.delet_product),

     path('edit_product/<pid>',views.edit_product),

     


     #________user______
     path('register',views.reg),
     path('',views.user_home)
]
