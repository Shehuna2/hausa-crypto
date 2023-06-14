from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField



# class PublisheManager(models.manager):
#     def get_queryset(self):
#         return super(PublisheManager,self).get_queryset().filter(status='published')

STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    category = models.ManyToManyField(Category, related_name='posts')
    body = RichTextUploadingField()
    image = models.ImageField(upload_to='featured_image/%Y/%M/%D/')
    tag = TaggableManager()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    
    # objects = models.Manager() # The default manager
    # published = PublisheManager() # Custome manager

    def get_absolute_url(self):
        return reverse('core:post-detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    body = models.TextField()

    class Meta:
        ordering = ('created',)

    def __str__(self) -> str:
        return self.body
    
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)



















