from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/register/", views.register, name="register"),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/maps/', views.MapListView.as_view(), name='dashboard-maps'),
    path('dashboard/maps/create/', views.MapCreateView.as_view(), name='map-create'),
    path('dashboard/maps/update/<pk>/', views.MapUpdateView.as_view(), name='map-update'),
    path('dashboard/maps/delete/<pk>/', views.MapDeleteView.as_view(), name='map-delete'),
    path('dashboard/maps/download/<pk>/', views.MapDownloadView, name='map-download'),
    path('dashboard/maps/<pk>/', views.MapDetailView.as_view(), name='map-detail'),
    path('search', views.search, name="search"),
    path('like/', views.like_map, name="like_map"),
    path('musicians/', views.musicians, name="musicians"),
    path('leveldesigners/', views.leveldesigners, name="leveldesigners"),
    path('testers/', views.testers, name="testers"),
    path('devs/', views.devs, name="devs"),
    path('trailer/', views.trailer, name="trailer"),
    path('influenceurs/', views.influenceurs, name="influenceurs"),
    path('others/', views.others, name="others"),
    path('follow/', views.follow, name="follow"),
    path('share/', views.share, name="share"),







] + static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
