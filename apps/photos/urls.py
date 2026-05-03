from django.urls import path
from .views import PhotoListView, PhotoDetailView, PhotoUploadView, PhotoDownloadZipView

urlpatterns = [
    path('', PhotoListView.as_view(), name='photo-list'),
    path('<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('upload/', PhotoUploadView.as_view(), name='photo-upload'),
    path('download-zip/', PhotoDownloadZipView.as_view(), name='photo-download-zip'),
]
