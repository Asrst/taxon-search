from django.urls import path
from . import views

app_name = "taxon_search"
urlpatterns = [
    path("", views.index, name="index"),
]
