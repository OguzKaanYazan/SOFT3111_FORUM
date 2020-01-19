from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.loginpage,name='loginpage'),
    path('logout/', views.logout,name='logout'),
    path('',views.homepageGuest, name='homepageGuest'),
    path('forum/', views.posts_list, name='posts_list'),
    path('news/', views.news, name='news'),
    path('post/<str:pk>/', views.post_detail, name='post_detail'),
    path('news/<str:pk>/', views.news_detail, name='news_detail'),
    path('store/' , views.store , name='store'),
    path('product/<int:pk>/', views.purchaseForm, name='purchaseForm'),
    path('upcomingEvents/', views.upcomingEvents, name='upcomingEvents'),
    path('post/new',views.new_post,name='new_post'),
    path('News/add', views.addNews, name='addNews'),
    path('product/new', views.AddProduct, name='addProduct'),
    path('event/add', views.addEvent, name='addEvent'),
    path('profile/', views.Profile, name='profile'),
    path('adminPanel/', views.Admin, name= 'adminPanel'),
    path('register/', views.Register, name='register'),
    path('upcomingEvents/<str:pk>/', views.event_detail, name='event_detail'),
    path('editProfile',views.editProfile, name='editProfile'),
    path('deletePost/<str:pk>/', views.deletePost, name='deletePost'),
    path('deleteProduct/<str:pk>/', views.deleteProduct, name ='deleteProduct'),
    path('shuttle/', views.shuttle, name='shuttle'),
    path('deleteShuttle/<int:pk>/', views.deleteShuttle,name = 'deleteShuttle'),
    path('addShuttle/', views.addShuttle, name='addShuttle'),
    path('courseNotes/', views.courseNotes, name= 'courseNotes'),
    path('pdf/<int:pk>/',views.pdf_view, name='pdf_views'),
    path('deleteNote/<int:pk>/', views.deleteNotes , name='deleteNote'),
    path('addNote/', views.addNotes, name='addNote')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
