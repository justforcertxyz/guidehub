from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.conf import settings
from django.core.files.storage import FileSystemStorage

html_storage = FileSystemStorage(location=settings.BLOG_HTML_ROOT)


class Blog(models.Model):
    title = models.CharField("Post Title", max_length=50, unique=True)
    slug = models.SlugField("Slug", max_length=50, unique=True)
    tags = TaggableManager()
    html_file = models.FileField("HTML File",
                                 storage=html_storage,
                                 null=True, blank=True
                                 )
    pub_date = models.DateTimeField("Date Published", default=timezone.now)

    def __str__(self):
        return self.title

    def template_path(self):
        return f"{str(settings.BLOG_HTML_ROOT).split("templates/")[1]}/{self.html_file.name}"
