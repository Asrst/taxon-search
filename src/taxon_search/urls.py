from django.urls import path
from . import views

app_name = "taxon_search"
urlpatterns = [
    path("", views.index, name="index"),
    path("tree/<str:taxon_id>/", views.taxon_tree, name="taxon_tree"),
]
