from django.urls import path
from .views import PhotoListView, PhotoDetailView, PhotoUploadView, PhotoDownloadSingleView, PhotoDownloadZipView

urlpatterns = [
    path('', PhotoListView.as_view(), name='photo-list'),
    path('<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('<int:pk>/download/', PhotoDownloadSingleView.as_view(), name='photo-download-single'),
    path('upload/', PhotoUploadView.as_view(), name='photo-upload'),
    path('download-zip/', PhotoDownloadZipView.as_view(), name='photo-download-zip'),
]
