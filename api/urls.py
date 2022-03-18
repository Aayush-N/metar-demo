from django.urls import path

app_name = "api"

from apps.main.apis import *

urlpatterns = [
	path('ping/', StatusCheck.as_view(), name='staus_check_api'),
]