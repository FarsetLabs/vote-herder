from django.urls import path

from .views import DemoView

app_name = "demo"


urlpatterns = [path("", DemoView.as_view(), name="demo")]
