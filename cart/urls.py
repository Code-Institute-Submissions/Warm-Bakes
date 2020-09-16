from django.urls import path,re_path
import cart.views

urlpatterns = [
    path('add/<lesson_id>',cart.views.add_lesson_to_cart,name="add_lesson_to_cart_route"),
    re_path(r'^add/(?P<product_id>[^/]+)/$',cart.views.add_product_to_cart,name="add_product_to_cart_route"),
    path('',cart.views.view_cart, name="view_cart_route"),
    path('remove/<lesson_id>',cart.views.remove_lesson_from_cart,name="remove_lesson_from_cart_route"),
    re_path(r'^remove/(?P<product_id>[^/]+)/$',cart.views.remove_product_from_cart,name="remove_product_from_cart_route"),
    re_path(r'^update_quantity/(?P<product_id>[^/]+)/$',cart.views.update_quantity_for_product,name="update_product_quantity_to_cart_route"),
]