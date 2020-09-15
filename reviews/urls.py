from django.urls import path,re_path
import reviews.views

urlpatterns=[
    path('',reviews.views.user_reviews,name="view_all_reviews_route"),
    path('create/<lesson_id>',reviews.views.create_lesson_review,name="create_lesson_review_route"),
    re_path(r'^create/(?P<product_id>[^/]+)/$',reviews.views.create_product_review,name='create_product_review_route')
]