from django.urls import path

from . import views

urlpatterns = [
    
    path("wiki/<str:name>", views.find, name="findwiki"),
    path("searchWiki", views.searchWiki, name="searchWiki"),
    path("newEntry", views.createPage,name="create"),
    path("editEntry/<str:name>",views.editPage,name="editPage"),
    path("random", views.randomPage, name="randomPage"),
    path("", views.index, name="index"),
    path("<str:name>", views.find, name="find")
    


]
