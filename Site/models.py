from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django_unique_slugify import unique_slugify

PAGE_TYPES = [("1", "Personal"), ("2", "Business")]

class Template(models.Model):
    name = models.CharField(max_length=255, null=True)
    content = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Circle(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Wall(models.Model):
    name = models.CharField(max_length=255)
    wall_link = models.SlugField(max_length=255, verbose_name='Wall Slug',blank=True, default="")
    public = models.BooleanField(default=False)
    about_page = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True, help_text="Please add meta tags by comma seperate")
    picture = models.URLField(null=True, max_length=255, blank=True)
    type = models.CharField(max_length=5, choices=PAGE_TYPES, default=1)
    topic = models.CharField(max_length=255, blank=True, null=True)
    # circles = models.CharField(max_length=255, blank=True, null=True)
    # topic = models.ManyToManyField(Topic, blank=True)
    circles = models.ManyToManyField(Circle, blank=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    template = models.ForeignKey(Template, related_name="template_%(class)s", on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_%(class)s", on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.wall_link:
            unique_slugify(self, self.wall_link, slug_field_name='wall_link')
        else:
            unique_slugify(self, self.name, slug_field_name='wall_link')
        super(Wall, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=255)
    is_editable = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    page = models.ForeignKey(Wall,
                              related_name="page_%(class)s",
                              null=True, blank=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SectionField(models.Model):
    type = models.CharField(max_length=255, null=True)
    url = models.URLField(null=True, max_length=255, blank=True)
    text = models.TextField(blank=True, null=True)
    position = models.IntegerField(default=0)
    section = models.ForeignKey(Section,
                                related_name="section_%(class)s",
                                null=True, blank=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.type


    def __str__(self):
        return self.type