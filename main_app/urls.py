from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home_page'),
    path('forum/',  views.to_forum, name = 'forum_home'),
    path('inscription/', views.subscription, name = 'subscription'),
    path('about-us', views.to_about, name = 'about-us'),
    path('contact-us', views.to_contact, name = 'contact-us'),
    path('profile/<slug:pseudoSlug>', views.to_profile, name='profile'),
    path(views.EMPLACEMENT_LIVRE + '/list', views.to_bookList, name = 'book-list'),
    path(views.EMPLACEMENT_LIVRE + '/<slug:bookSlug>', views.to_book, name = "book"),
    path('login', views.to_login, name = 'login'),
    path('desc', views.to_desc, name='desc'),
    path('listing', views.to_listing, name='listing'),
]

#EMPLACEMENT_LIVRE = "book/"