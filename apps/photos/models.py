from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/original/')
    watermarked = models.ImageField(upload_to='photos/watermarked/', blank=True)
    original_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name or str(self.id)
