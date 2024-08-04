from django.db import models

class OCRResult(models.Model):
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
