from django.db import models

class AltTextInfo(models.Model):
    excel_file = models.FileField(upload_to='uploads/')
    # You might need to add more fields depending on your requirements
