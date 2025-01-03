from django.urls import path
from . import views

urlpatterns = [
     path('loge', views.log),
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
     path('home',views.user_home),
     path('shop',views.shop),
     path('viewpro/<pid>',views.viewpro),
     path('cart/<pid>',views.add_to_cart),
     path('qty-dic/<cid>',views.qty_dec),
     path('qty-in/<cid>',views.qty_in),
     path('my_cart',views.view_cart),
     path('delete_cartitem/<int:id>', views.delete_cart_item,name='delete_cartitem' ),
     path('booking/<pid>',views.bookings,name='bookings'),
     path('address/<pid>/<aid>',views.add_adress),
]
