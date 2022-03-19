from django.urls import path

from .views import LandingPageView

app_name = "main"

urlpatterns = [
	path("", view=LandingPageView.as_view(), name="landing_page"),
]
