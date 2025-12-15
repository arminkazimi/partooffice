# myapp/models.py
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class SingletonModel(models.Model):
    """Abstract base class for singleton models"""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Delete all other instances if they exist
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Get or create the single instance"""
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls.objects.create()


class AboutMe(SingletonModel):
    caption = models.TextField()
    photo = models.ImageField(upload_to='about/')
    document = models.FileField(upload_to='products/', null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "About Me"  # Nice admin name

    def __str__(self):
        return self.title


class ContactMe(SingletonModel):
    mobile = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    email1 = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Me"  # Nice admin name

    def __str__(self):
        return f'{self.mobile}, {self.phone}, {self.email1}, {self.email2}'


# class DesignOrder(models.Model):
#     pass


class Education(models.Model):
    tilte = models.CharField(max_length=200)
    caption = models.TextField(null=True, blank=True, default="No caption provided")
    url = models.URLField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductDoc(SingletonModel):
    application = models.FileField(upload_to='products/', null=True, blank=True)
    presentation = models.FileField(upload_to='products/', null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product docs"  # Nice admin name

    def __str__(self):
        app_name = self.application.name.split('/')[-1] if self.application else "No application"
        pres_name = self.presentation.name.split('/')[-1] if self.presentation else "No presentation"
        return f"Application: {app_name}, Presentation: {pres_name}"


class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    caption = models.TextField(null=True, blank=True, default="No caption provided")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['created_at']

    def __str__(self):
        img_name = self.image.name.split('/')[-1] if self.image else "No image"
        caption_preview = (self.caption[:15] + '...') if self.caption and len(self.caption) > 15 else (
                self.caption or "No caption")
        return f"Image: {img_name}, Caption: {caption_preview}"


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

    # thumbnail = models.OneToOneField(
    #     'ProjectImage',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='main_thumbnail'
    # )
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    caption = models.TextField(null=True, blank=True, default="No caption provided")

    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.project.name} - {self.caption or self.image.name}"
        return f"{self.caption or self.image.name}"


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
    caption = models.TextField(null=True, blank=True, default="No caption provided")

    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.event.name} - {self.caption or self.image.name}"
        return f"{self.caption or self.image.name}"


class Job(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)



@receiver(pre_delete, sender=ProjectImage)
def handle_image_deletion(sender, instance, **kwargs):
    """Update thumbnail when image is deleted"""
    project = instance.project
    if project.thumbnail == instance:
        project.update_thumbnail()


@receiver(pre_delete, sender=EventImage)
def handle_image_deletion(sender, instance, **kwargs):
    """Update thumbnail when image is deleted"""
    event = instance.event
    if event.thumbnail == instance:
        event.update_thumbnail()
