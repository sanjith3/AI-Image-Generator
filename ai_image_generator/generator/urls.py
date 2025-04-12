from django.urls import path
from . import views  # Import views from the same app
from .views import generate_view, download_image, history_view

urlpatterns = [
    path('', views.generate_view, name='generate'),
    path('download/<int:image_id>/', download_image, name='download_image'),# Root for this app
    path('history/', views.history_view, name='history'),
]
