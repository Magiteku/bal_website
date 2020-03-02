from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home_page'),
    path('forum/',  views.to_forum, name = 'forum_home'),
    path('inscription/', views.to_subscription, name = 'subscription'),
    path('about-us', views.to_about, name = 'about-us'),
    path('contact-us', views.to_contact, name = 'contact-us'),
    path(views.EMPLACEMENT_LIVRE + '/list', views.to_bookList, name = 'book-list'),
    path(views.EMPLACEMENT_LIVRE + '/<slug:bookSlug>', views.to_book, name = "book"),
] 

#EMPLACEMENT_LIVRE = "book/"