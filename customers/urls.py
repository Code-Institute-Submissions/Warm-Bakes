from django.urls import path
import customers.views

urlpatterns=[
    path("myprofile/",customers.views.show_user_profile,name="profile_page_route"),
    path("profile/update/<user_id>",customers.views.update_profile,name="update_profile_page_route")
]