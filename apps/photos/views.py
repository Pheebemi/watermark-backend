import os
import io
import zipfile

from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Photo
from .serializers import PhotoSerializer
from .utils import add_church_watermark


class PhotoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        photos = Photo.objects.all().order_by('-created_at')
        serializer = PhotoSerializer(photos, many=True, context={'request': request})
        return Response({"success": True, "data": serializer.data})


class PhotoDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            photo = Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            return Response({"success": False, "error": "Photo not found"}, status=404)
        serializer = PhotoSerializer(photo, context={'request': request})
        return Response({"success": True, "data": serializer.data})


class PhotoUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        files = request.FILES.getlist('images')

        if not files:
            return Response({"success": False, "error": "No files provided"}, status=400)

        if len(files) > 30:
            return Response({"success": False, "error": "Maximum 30 images per upload"}, status=400)

        results = []
        errors = []

        for file in files:
            try:
                photo = Photo.objects.create(image=file, original_name=file.name)

                watermarked_filename = f"wm_{photo.id}_{file.name}"
                watermarked_path = os.path.join(
                    settings.MEDIA_ROOT, 'photos', 'watermarked', watermarked_filename
                )

                add_church_watermark(
                    photo_path=photo.image.path,
                    logo_path=str(settings.CHURCH_LOGO_PATH),
                    output_path=watermarked_path
                )

                photo.watermarked = f"photos/watermarked/{watermarked_filename}"
                photo.save()

                results.append({
                    "id": photo.id,
                    "original_name": photo.original_name,
                    "watermarked_url": request.build_absolute_uri(photo.watermarked.url)
                })

            except Exception as e:
                errors.append({"file": file.name, "error": str(e)})

        return Response({
            "success": True,
            "data": {"processed": results, "errors": errors, "total": len(results)}
        })


class PhotoDownloadZipView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        photo_ids = request.data.get('ids', [])

        if not photo_ids:
            return Response({"success": False, "error": "No photo IDs provided"}, status=400)

        photos = Photo.objects.filter(id__in=photo_ids)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for photo in photos:
                if photo.watermarked and os.path.exists(photo.watermarked.path):
                    zip_file.write(
                        photo.watermarked.path,
                        arcname=f"{photo.original_name or photo.id}.jpg"
                    )

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="church_photos.zip"'
        return response
