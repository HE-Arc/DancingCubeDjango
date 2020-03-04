from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/register/", views.register, name="register"),  # <-- added
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/maps/', views.MapListView.as_view(), name='dashboard-maps'),
    path('dashboard/maps/create/', views.MapCreateView.as_view(), name='map-create'),
    path('dashboard/maps/update/<pk>/', views.MapUpdateView.as_view(), name='map-update'),
    path('dashboard/maps/delete/<pk>/', views.MapDeleteView.as_view(), name='map-delete'),
    path('dashboard/maps/<pk>/', views.MapDetailView.as_view(), name='map-detail'),
]
