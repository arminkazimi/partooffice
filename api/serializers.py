from rest_framework import serializers

from portfolio.models import (
    AboutMe,
    ContactMe,
    # DesignOrder,
    Education,
    Project,
    ProjectImage,
    ProductDoc,
    Product,
    Event,
    EventImage, Job,
)


class AboutMeSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutMe
        fields = ("id", "caption", "photo_url", "document_url", "updated_at", "created_at")

    def get_photo_url(self, obj):
        if not obj.photo:
            return None
        request = self.context.get("request")
        url = obj.photo.url
        return request.build_absolute_uri(url) if request else url

    def get_document_url(self, obj):
        if not obj.document:
            return None
        request = self.context.get("request")
        url = obj.document.url
        return request.build_absolute_uri(url) if request else url

class ContactMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMe
        fields = ("id", "mobile", "phone", "email1", "email2", "updated_at", "created_at")
        read_only_fields = ("updated_at", "created_at", "id")


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        # Using the actual field name 'tilte' to match your model as posted.
        fields = ("id", "tilte", "caption", "url", "updated_at", "created_at")
        read_only_fields = ("id", "updated_at", "created_at")
class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ("id", "image_url", "caption", "uploaded_at")

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "status",
            "status_display",
            "usage",
            "project_date",
            "created_at",
            "updated_at",
            "thumbnail_url",
            "images",
        )

    def get_thumbnail_url(self, obj):
        thumbnail = getattr(obj, "thumbnail", None)

        if not thumbnail:
            return None

        try:
            url = thumbnail.url
        except ValueError:
            return None

        request = self.context.get("request")
        return request.build_absolute_uri(url) if request else url


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "image_url", "caption")

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class ProductDocSerializer(serializers.ModelSerializer):
    application_url = serializers.SerializerMethodField()
    presentation_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductDoc
        fields = ("id", "application_url", "presentation_url", "updated_at", "created_at")
        read_only_fields = ("id", "updated_at", "created_at")

    def _build_url(self, field_file):
        if not field_file:
            return None
        request = self.context.get("request")
        url = field_file.url
        return request.build_absolute_uri(url) if request else url

    def get_application_url(self, obj):
        return self._build_url(getattr(obj, "application", None))

    def get_presentation_url(self, obj):
        return self._build_url(getattr(obj, "presentation", None))


class EventImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EventImage
        fields = ("id", "image_url", "caption", "uploaded_at", "created_at")
        read_only_fields = ("id", "uploaded_at", "created_at")

    def get_image_url(self, obj):
        img = getattr(obj, "image", None)
        if not img:
            return None
        request = self.context.get("request")
        url = img.url
        return request.build_absolute_uri(url) if request else url


class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "status",
            "status_display",
            "usage",
            "event_date",
            "created_at",
            "updated_at",
            "thumbnail_url",
            "images",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_thumbnail_url(self, obj):
        thumb = getattr(obj, "thumbnail", None)
        if not thumb or not getattr(thumb, "image", None):
            return None
        request = self.context.get("request")
        url = thumb.image.url
        return request.build_absolute_uri(url) if request else url


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        # allow client to provide name, email, phone_number
        fields = ("id", "name", "email", "phone_number", "uploaded_at", "created_at")
        read_only_fields = ("id", "uploaded_at", "created_at")

    # optional: add simple phone validation (adjust to your needs)
    def validate_phone_number(self, value):
        value = value.strip()
        if len(value) < 10:  # very basic check
            raise serializers.ValidationError("Phone number is too short.")
        return value