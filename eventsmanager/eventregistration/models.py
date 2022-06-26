from django.db import models

from eventcreation.models import Event
from django.contrib.auth.models import User

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
# Create your models here.

class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qrcode = models.ImageField(blank=True, upload_to='code')

    def save(self, *args, **kwargs):
        qr_code = qrcode.make(f'{self.event.name}{self.user.username}')
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(qr_code)
        file_name = f'{self.event.name}-{self.user.username}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qrcode.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.event} - {self.user}'