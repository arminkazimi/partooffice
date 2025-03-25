# myapp/admin.py
from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import AboutMe, ProductImage, Product, Event, EventImage, ContactMe
from .models import Project, ProjectImage


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('updated_at', 'photo_preview')

    def photo_preview(self, obj):
        return obj.photo and mark_safe(f'<img src="{obj.photo.url}" style="max-height: 200px;" />')

    photo_preview.short_description = "Preview"

    def changelist_view(self, request, extra_context=None):
        # Redirect directly to change form if only one object exists
        if AboutMe.objects.count() == 1:
            obj = AboutMe.objects.first()
            return redirect(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', obj.id)
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        # Disable "Add" button if entry exists
        return not AboutMe.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the single entry
        return False


@admin.register(ContactMe)
class ContactMeAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'phone', 'email1', 'email2')
    readonly_fields = ('updated_at',)

    def changelist_view(self, request, extra_context=None):
        # Redirect directly to change form if only one object exists
        if ContactMe.objects.count() == 1:
            obj = ContactMe.objects.first()
            return redirect(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', obj.id)
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        # Disable "Add" button if entry exists
        return not ContactMe.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the single entry
        return False


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" style="max-height: 100px;" />')
        return "No image"

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('description', 'updated_at')

    def has_add_permission(self, request):
        return not Product.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if Product.objects.count() == 1:
            obj = Product.objects.first()
            return redirect(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', obj.id)
        return super().changelist_view(request, extra_context)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk and not cleaned_data.get('thumbnail'):
            if not self.instance.images.exists():
                raise forms.ValidationError(
                    "You must have at least one image for existing projects"
                )
        return cleaned_data


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    min_num = 1
    extra = 2
    fields = ('image', 'caption', 'is_thumbnail')
    readonly_fields = ('is_thumbnail',)

    def is_thumbnail(self, obj):
        return obj == obj.project.thumbnail

    is_thumbnail.boolean = True
    is_thumbnail.short_description = 'Is Thumbnail'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    inlines = [ProjectImageInline]
    list_display = ('name', 'status_display', 'thumbnail_preview', 'project_date')
    list_filter = ('status', 'project_date')
    search_fields = ('name', 'usage')
    readonly_fields = ('thumbnail_preview', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'status', 'usage', 'project_date')
        }),
        ('Thumbnail Selection', {
            'fields': ('thumbnail',),
            'classes': ('collapse',),
            'description': 'Select from uploaded images below'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Automatically managed dates'
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail and obj.thumbnail.image:
            return format_html('<img src="{}" style="max-height: 50px;">', obj.thumbnail.image.url)
        return "No thumbnail"

    thumbnail_preview.short_description = 'Preview'

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = 'Status'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['thumbnail'].queryset = obj.images.all()
        else:
            form.base_fields['thumbnail'].widget = forms.HiddenInput()
            form.base_fields['thumbnail'].required = False
        return form

    def save_model(self, request, obj, form, change):
        # First save to create primary key
        super().save_model(request, obj, form, change)
        if not change:
            obj.refresh_from_db()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        project = form.instance

        if not change and project.images.exists():
            if not project.thumbnail:
                project.thumbnail = project.images.first()
                project.save(update_fields=['thumbnail'])

        # Validate thumbnail belongs to project
        if project.thumbnail and project.thumbnail not in project.images.all():
            project.thumbnail = None
            project.save(update_fields=['thumbnail'])

    def delete_queryset(self, request, queryset):
        """Handle bulk deletion"""
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        """Handle single deletion"""
        obj.delete()


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk and not cleaned_data.get('thumbnail'):
            if not self.instance.images.exists():
                raise forms.ValidationError(
                    "You must have at least one image for existing projects"
                )
        return cleaned_data


class EventImageInline(admin.TabularInline):
    model = EventImage
    min_num = 1
    extra = 2
    fields = ('image', 'caption', 'is_thumbnail')
    readonly_fields = ('is_thumbnail',)

    def is_thumbnail(self, obj):
        return obj == obj.event.thumbnail

    is_thumbnail.boolean = True
    is_thumbnail.short_description = 'Is Thumbnail'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm
    inlines = [EventImageInline]
    list_display = ('name', 'status_display', 'thumbnail_preview', 'event_date')
    list_filter = ('status', 'event_date')
    search_fields = ('name', 'usage')
    readonly_fields = ('thumbnail_preview', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'status', 'usage', 'event_date')
        }),
        ('Thumbnail Selection', {
            'fields': ('thumbnail',),
            'classes': ('collapse',),
            'description': 'Select from uploaded images below'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Automatically managed dates'
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail and obj.thumbnail.image:
            return format_html('<img src="{}" style="max-height: 50px;">', obj.thumbnail.image.url)
        return "No thumbnail"

    thumbnail_preview.short_description = 'Preview'

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = 'Status'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['thumbnail'].queryset = obj.images.all()
        else:
            form.base_fields['thumbnail'].widget = forms.HiddenInput()
            form.base_fields['thumbnail'].required = False
        return form

    def save_model(self, request, obj, form, change):
        # First save to create primary key
        super().save_model(request, obj, form, change)
        if not change:
            obj.refresh_from_db()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        event = form.instance

        if not change and event.images.exists():
            if not event.thumbnail:
                event.thumbnail = event.images.first()
                event.save(update_fields=['thumbnail'])

        # Validate thumbnail belongs to event
        if event.thumbnail and event.thumbnail not in event.images.all():
            event.thumbnail = None
            event.save(update_fields=['thumbnail'])

    def delete_queryset(self, request, queryset):
        """Handle bulk deletion"""
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        """Handle single deletion"""
        obj.delete()

#
# @admin.register(EventImage)
# class EventImageAdmin(admin.ModelAdmin):
#     list_display = ('event', 'image_preview', 'caption', 'uploaded_at')
#     list_filter = ('event', 'uploaded_at')
#     readonly_fields = ('image_preview',)
#
#     def image_preview(self, obj):
#         return format_html('<img src="{}" style="max-height: 100px;">', obj.image.url)
#
#     image_preview.short_description = "Preview"
#
#     def delete_queryset(self, request, queryset):
#         """Handle bulk image deletion"""
#         events_to_update = set()
#         for img in queryset:
#             if img.event.thumbnail == img:
#                 events_to_update.add(img.event)
#         super().delete_queryset(request, queryset)
#         for event in events_to_update:
#             event.update_thumbnail()
#
#     def delete_model(self, request, obj):
#         """Handle single image deletion"""
#         needs_update = obj.event.thumbnail == obj
#         super().delete_model(request, obj)
#         if needs_update:
#             obj.event.update_thumbnail()
