from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/maps', views.MapListView.as_view(), name='dashboard-maps'),
    path('dashboard/maps/<pk>/', views.MapDetailView.as_view(), name='map-detail'),
]
