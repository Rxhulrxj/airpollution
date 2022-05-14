from django.urls import path,include
from . import views
urlpatterns=[
    path('',views.dashboard,name="dashboard"),
    path('feed/',views.index,name="feed"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("adminpage/",views.admin,name="adminpage"),
    path('logout',views.exituser,name="auth_logout")

]