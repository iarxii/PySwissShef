from django.db import models

class AutomationScript(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('data', 'Data Processing'),
        ('excel', 'Excel Migration'),
        ('sentiment', 'Sentiment Analysis'),
        ('sql', 'SQL Tools'),
        ('uncategorized', 'Uncategorized'),
    ],default='uncategorized')
    script_file = models.FileField(upload_to='scripts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name