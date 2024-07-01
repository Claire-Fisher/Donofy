from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Charity(models.Model):

    class Meta:
        verbose_name_plural = 'Charities'

    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=False)
    charity_name = models.CharField(max_length=254)
    charity_num = models.PositiveIntegerField()
    description = models.TextField()
    website_url = models.URLField(max_length=1024, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image_description = models.CharField(max_length=254, null=True, blank=True)
    logo_image = models.ImageField(null=True, blank=True)
    impact1 = models.TextField(null=True, blank=True)
    impact2 = models.TextField(null=True, blank=True)
    impact3 = models.TextField(null=True, blank=True)
    total_received_monthly = models.JSONField(blank=True)
    total_received = models.PositiveIntegerField(
        default=0, null=True, blank=True
    )

    def __str__(self):
        return self.charity_name
