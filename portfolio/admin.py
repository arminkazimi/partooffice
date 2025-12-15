# myapp/admin.py
from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    AboutMe, ProductDoc, Product, Event, EventImage, ContactMe,
    Project, ProjectImage, Education, Job
)


admin.site.site_header = "Parto Office Admin"
admin.site.site_title = "Parto Office Admin Portal"
admin.site.index_title = "Welcome to Parto Office Admin"


#
# Helper / base admin for singletons
#
class SingletonAdmin(admin.ModelAdmin):
    """
    Base admin for SingletonModel subclasses.
    - Redirect list view to change view when exactly 1 instance exists.
    - Prevent add/delete from the admin UI when an instance exists.
    """
    readonly_fields = ('updated_at', 'created_at')

    def changelist_view(self, request, extra_context=None):
        qs = self.model.objects.all()
        if qs.count() == 1:
            obj = qs.first()
            return redirect(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', obj.id)
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        # Allow add only if no instance exists
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion through admin UI
        return False


#
# AboutMe admin
#
@admin.register(AboutMe)
class AboutMeAdmin(SingletonAdmin):
    list_display = ('short_caption', 'updated_at')
    readonly_fields = ('updated_at', 'created_at', 'photo_preview',)

    def photo_preview(self, obj):
        if obj.photo and getattr(obj.photo, 'url', None):
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 200px;" />')
        return "No photo"
    photo_preview.short_description = "Photo preview"

    def short_caption(self, obj):
        return (obj.caption[:60] + '...') if obj.caption and len(obj.caption) > 60 else (obj.caption or "")
    short_caption.short_description = "Caption"


#
# ContactMe admin
#
@admin.register(ContactMe)
class ContactMeAdmin(SingletonAdmin):
    list_display = ('mobile', 'phone', 'email1', 'email2')
    readonly_fields = ('updated_at', 'created_at')


#
# ProductDoc admin (singleton)
#
@admin.register(ProductDoc)
class ProductDocAdmin(SingletonAdmin):
    list_display = ('application_name', 'presentation_name', 'updated_at')
    readonly_fields = ('updated_at', 'created_at')

    def application_name(self, obj):
        return obj.application.name.split('/')[-1] if obj.application else "No application"
    application_name.short_description = "Application"

    def presentation_name(self, obj):
        return obj.presentation.name.split('/')[-1] if obj.presentation else "No presentation"
    presentation_name.short_description = "Presentation"


#
# Product admin (keeps behaviour from your old admin: only one product in admin)
#
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('caption_preview', 'updated_at')
    readonly_fields = ('updated_at', 'created_at')

    def caption_preview(self, obj):
        if not obj.caption:
            return "No caption"
        return (obj.caption[:40] + '...') if len(obj.caption) > 40 else obj.caption
    caption_preview.short_description = "Caption"

    def has_add_permission(self, request):
        # keep previous behaviour (only allow one Product in admin)
        return not Product.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if Product.objects.count() == 1:
            obj = Product.objects.first()
            return redirect(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', obj.id)
        return super().changelist_view(request, extra_context)


#
# Education admin
#
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'url', 'created_at')
    search_fields = ('tilte', 'caption')  # note: model field is 'tilte' in your models
    readonly_fields = ('created_at', 'updated_at')

    def display_title(self, obj):
        # tolerant display even if field name is odd
        return getattr(obj, 'tilte', None) or "(no title)"
    display_title.short_description = "Title"


#
# Job admin
#
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'created_at')
    search_fields = ('name', 'email', 'phone_number')


#
# Project & ProjectImage inline
#
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    min_num = 1
    extra = 2
    fields = ('image', 'caption', 'is_thumbnail')
    readonly_fields = ('is_thumbnail',)

    def is_thumbnail(self, obj):
        # obj may be None for the "empty" inline forms
        try:
            project_thumbnail = obj.project.thumbnail
            return obj and project_thumbnail and (obj.id == project_thumbnail.id)
        except Exception:
            return False
    is_thumbnail.boolean = True
    is_thumbnail.short_description = 'Is Thumbnail'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        # if editing existing project and no thumbnail set, ensure at least one image exists
        if self.instance.pk and not cleaned_data.get('thumbnail'):
            if not self.instance.images.exists():
                raise forms.ValidationError("You must have at least one image for existing projects")
        return cleaned_data


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    inlines = [ProjectImageInline]
    list_display = ('name', 'status_display', 'thumbnail_preview', 'project_date', 'created_at')
    list_filter = ('status', 'project_date')
    search_fields = ('name', 'usage')
    readonly_fields = ('thumbnail_preview', 'created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('name', 'status', 'usage', 'project_date')}),
        ('Thumbnail Selection', {
            'fields': ('thumbnail',),
            'classes': ('collapse',),
            'description': 'Select an uploaded image as thumbnail (if left blank, first image will be used)'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def thumbnail_preview(self, obj):
        if obj and obj.thumbnail and getattr(obj.thumbnail, 'image', None):
            return format_html('<img src="{}" style="max-height: 50px;">', obj.thumbnail.image.url)
        return "No thumbnail"
    thumbnail_preview.short_description = 'Preview'

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # limit thumbnail choices to this project's images only
            form.base_fields['thumbnail'].queryset = obj.images.all()
        else:
            # hide thumbnail field for new objects until images are uploaded
            form.base_fields['thumbnail'].widget = forms.HiddenInput()
            form.base_fields['thumbnail'].required = False
        return form

    def save_model(self, request, obj, form, change):
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

        # Ensure thumbnail belongs to project images
        if project.thumbnail and project.thumbnail not in project.images.all():
            project.thumbnail = None
            project.save(update_fields=['thumbnail'])

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        obj.delete()


#
# Event & EventImage inline
#
class EventImageInline(admin.TabularInline):
    model = EventImage
    min_num = 1
    extra = 2
    fields = ('image', 'caption', 'is_thumbnail')
    readonly_fields = ('is_thumbnail',)

    def is_thumbnail(self, obj):
        try:
            event_thumbnail = obj.event.thumbnail
            return obj and event_thumbnail and (obj.id == event_thumbnail.id)
        except Exception:
            return False
    is_thumbnail.boolean = True
    is_thumbnail.short_description = 'Is Thumbnail'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk and not cleaned_data.get('thumbnail'):
            if not self.instance.images.exists():
                raise forms.ValidationError("You must have at least one image for existing events")
        return cleaned_data


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm
    inlines = [EventImageInline]
    list_display = ('name', 'status_display', 'thumbnail_preview', 'event_date', 'created_at')
    list_filter = ('status', 'event_date')
    search_fields = ('name', 'usage')
    readonly_fields = ('thumbnail_preview', 'created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('name', 'status', 'usage', 'event_date')}),
        ('Thumbnail Selection', {
            'fields': ('thumbnail',),
            'classes': ('collapse',),
            'description': 'Select an uploaded image as thumbnail (if left blank, first image will be used)'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def thumbnail_preview(self, obj):
        if obj and obj.thumbnail and getattr(obj.thumbnail, 'image', None):
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

        # Validate thumbnail belongs to event images
        if event.thumbnail and event.thumbnail not in event.images.all():
            event.thumbnail = None
            event.save(update_fields=['thumbnail'])

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        obj.delete()
