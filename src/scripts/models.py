from django.db import models

class AutomationScript(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    script_file = models.FileField(upload_to='scripts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name