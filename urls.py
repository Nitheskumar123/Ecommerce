from django.urls import path,include
from ecommerce import views
urlpatterns = [
    path('',views.index,name='home'),
    path('register',views.register,name='register'),
    path('collections',views.collections,name='collections'),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('product/<str:name>', views.productview, name='product'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('update',views.update,name='update'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('cart',views.cart,name='cart'),
    path('removecart/<str:id>',views.removecart,name='removecart'),
    path('checkout',views.checkout,name='checkout'),
    path('place-order',views.placeorder,name='placeorder'),
    path('proceed-to-pay',views.razorpaycheck),
   path('my-orders', views.myorders, name='my-orders'),
   path('view-order/<str:trackno>',views.vieworder,name='orderview'),
   path('download-pdf/<int:order_id>/', views.generate_pdf, name='download_pdf'),
   
   path('products/', views.product_list, name='product-list'),
    

]
