from django.db import models
from django.utils.timezone import now

class GeneratedImage(models.Model):
    prompt = models.TextField()
    image = models.ImageField(upload_to='generated/')
    timestamp = models.DateTimeField(default=now)  # Add this field

    def __str__(self):
        return f"Image generated for '{self.prompt}'"
