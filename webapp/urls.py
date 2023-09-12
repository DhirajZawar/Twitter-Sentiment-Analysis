from django.urls import path
from webapp import views

app_name = "webapp"

urlpatterns = [

	path("", views.Home, name="home"),

	path("signup/", views.Signup, name="signup"),
	path("signin/", views.Signin, name="signin"),
	path("signout/", views.Signout, name="signout"),

]