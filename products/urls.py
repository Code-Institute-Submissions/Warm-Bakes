from django.urls import path
import products.views

urlpatterns = [
    path('', products.views.show_all_products,name="show_all_products_route"),
    path('inventory/',products.views.products_inventory, name="product_inventory_route"),
    path('detail/<product_id>',products.views.show_product_detail),
    path('create/',products.views.create_product, name="create_product_route"),
    path('edit/<product_id>',products.views.update_product, name="update_product_route"),
    path('delete/<product_id>',products.views.delete_product, name="delete_product_route"),
    path('category/delete/<category_id>',products.views.delete_category,name="delete_category_route")
]