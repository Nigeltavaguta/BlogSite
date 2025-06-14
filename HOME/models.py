from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.utils import timezone
from PIL import Image
import os

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f'{base_slug}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    is_guest = models.BooleanField(default=False, help_text="Check if this is a guest author.")
    profile_image = models.ImageField(upload_to='author_images', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to generate file path
        if self.profile_image:
            # Open and resize image
            img = Image.open(self.profile_image.path)
            if img.height != 32 or img.width != 32:
                output_size = (32, 32)
                img.thumbnail(output_size, Image.LANCZOS)
                img.save(self.profile_image.path, format='JPEG', quality=85)

    def __str__(self):
        return self.name if not self.is_guest else "Guest"

class Blog(models.Model):
    STATUS = (
        ('0', 'DRAFT'),
        ('1', 'PUBLISH')
    )
    SECTION = (
        ('Recent', 'Recent'),
        ('Popular', 'Popular'),
        ('Trending', 'Trending'),
        ('EditorsPick', 'EditorsPick'),
        ('Inspiration', 'Inspiration'),
        ('Celebration', 'Celebration'),
    )
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='blogs', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    blog_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=1, default='0')
    section = models.CharField(choices=SECTION, max_length=100)
    Main_post = models.BooleanField(default=False)
    views = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.title} ({self.category})'
    
    @property
    def excerpt(self):
        return ' '.join(self.content.split()[:20]) + '...'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    blog_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    comment = models.TextField()
    date = models.DateField(default=timezone.now)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="replies")

    def save(self, *args, **kwargs):
        if self.post:
            self.blog_id = self.post_id
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name