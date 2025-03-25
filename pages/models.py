# myapp/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class AboutMe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='about/')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About Me"  # Nice admin name

    def save(self, *args, **kwargs):
        if not self.pk and AboutMe.objects.exists():
            # Prevent creating new entries if one already exists
            raise ValidationError("Only one AboutMe entry allowed")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContactMe(models.Model):
    mobile = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    email1 = models.EmailField(blank=True,null=True)
    email2 = models.EmailField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact Me"  # Nice admin name

    def save(self, *args, **kwargs):
        if not self.pk and ContactMe.objects.exists():
            # Prevent creating new entries if one already exists
            raise ValidationError("Only one ContactMe entry allowed")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.mobile}, {self.phone}, {self.email1}, {self.email2}'


class Product(models.Model):
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and Product.objects.exists():
            raise ValidationError("Only one product configuration is allowed")
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'PL', _('Planned')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETED = 'CO', _('Completed')
        ON_HOLD = 'OH', _('On Hold')
        CANCELLED = 'CL', _('Cancelled')

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PLANNED
    )
    usage = models.CharField(max_length=255)
    project_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.OneToOneField(
        'ProjectImage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_thumbnail'
    )

    def __str__(self):
        return self.name

    def update_thumbnail(self):
        """Update thumbnail to first available image or None"""
        self.thumbnail = self.images.first()
        self.save(update_fields=['thumbnail'])


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='projects/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.project.name} - {self.caption or self.image.name}"
        return f"{self.caption or self.image.name}"


@receiver(pre_delete, sender=ProjectImage)
def handle_image_deletion(sender, instance, **kwargs):
    """Update thumbnail when image is deleted"""
    project = instance.project
    if project.thumbnail == instance:
        project.update_thumbnail()


class Event(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'PL', _('Planned')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETED = 'CO', _('Completed')
        ON_HOLD = 'OH', _('On Hold')
        CANCELLED = 'CL', _('Cancelled')

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PLANNED
    )
    usage = models.CharField(max_length=255)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.OneToOneField(
        'EventImage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_thumbnail'
    )

    def __str__(self):
        return self.name

    def update_thumbnail(self):
        """Update thumbnail to first available image or None"""
        self.thumbnail = self.images.first()
        self.save(update_fields=['thumbnail'])


class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='events/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.event.name} - {self.caption or self.image.name}"
        return f"{self.caption or self.image.name}"


@receiver(pre_delete, sender=EventImage)
def handle_image_deletion(sender, instance, **kwargs):
    """Update thumbnail when image is deleted"""
    event = instance.event
    if event.thumbnail == instance:
        event.update_thumbnail()
