from django.db import models

class AutomationScript(models.Model):
    ENVIRONMENT_CHOICES = [
        ('sb', 'StackBlitz (Light)'),
        ('cs', 'Codespaces (Standard)'),
        ('rp', 'Replit (Heavy)'),
        ('lr', 'Local Recommended'),
    ]

    SECURITY_CHOICES = [
        ('low', 'Low-Impact (Utility)'),
        ('high', 'High-Access (System)'),
        ('exp', 'Experimental'),
    ]

    CATEGORY_CHOICES = [
        ('data', 'Data Processing'),
        ('nlp', 'Natural Language'),
        ('web', 'Web Automation'),
        ('sql', 'SQL Tools'),
        ('uncategorized', 'Uncategorized'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    detailed_description = models.TextField(blank=True, help_text="The Gourmet Story/Recipe documentation")
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='uncategorized')
    
    # GitHub Integration
    repo_url = models.URLField(blank=True, help_text="Link to GitHub repository")
    release_url = models.URLField(blank=True, help_text="Link to latest release download")
    
    # Environment & Performance
    environment_target = models.CharField(max_length=2, choices=ENVIRONMENT_CHOICES, default='sb')
    has_sample_data = models.BooleanField(default=False, help_text="Can be run with pre-bundled sample files")
    
    # Security
    security_level = models.CharField(max_length=4, choices=SECURITY_CHOICES, default='low')
    security_disclaimer = models.TextField(blank=True, help_text="Specific security concerns for this script")

    script_file = models.FileField(upload_to='scripts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name