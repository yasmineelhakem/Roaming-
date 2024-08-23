from django.db import models

# Create your models here.

class RoamingIn(models.Model):
    input_file = models.FileField(upload_to='roaming_in_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roaming IN - {self.input_file.name}"

class RoamingOut(models.Model):
    input_file = models.FileField(upload_to='roaming_out_files/inputs',null=True)
    output_file = models.FileField(upload_to='roaming_out_files/outputs', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roaming OUT - {self.input_file.name}"