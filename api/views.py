# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from portfolio.models import Project, AboutMe, ContactMe, Education, ProductDoc, Product, Event, Job, DesignOrder
from .serializers import ProjectSerializer, AboutMeSerializer, ContactMeSerializer, EducationSerializer, \
    ProductDocSerializer, ProductSerializer, EventSerializer, JobCreateSerializer


class AboutMeAPIView(generics.GenericAPIView):
    """
    GET /api/about/  -> returns the single AboutMe instance (or 404)
    Useful because AboutMe inherits SingletonModel.
    """
    serializer_class = AboutMeSerializer
    permission_classes = [permissions.AllowAny]
    queryset = AboutMe.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        if not obj:
            return Response({"detail": "AboutMe not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(obj, context={"request": request})
        return Response(serializer.data)


class ContactMeAPIView(generics.GenericAPIView):
    """
    GET /api/contact/ -> returns the single ContactMe instance (or 404)
    """
    serializer_class = ContactMeSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ContactMe.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        if not obj:
            return Response({"detail": "Contact information not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(obj, context={"request": request})
        return Response(serializer.data)


class EducationListAPIView(generics.ListAPIView):
    """
    GET /api/educations/  -> list of education entries (GET only)
    """
    queryset = Education.objects.all().order_by("-created_at")
    serializer_class = EducationSerializer
    permission_classes = [permissions.AllowAny]


class ProductDocAPIView(generics.GenericAPIView):
    """
    GET /api/product-doc/ -> returns the single ProductDoc instance (or 404)
    """
    serializer_class = ProductDocSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ProductDoc.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        if not obj:
            return Response({"detail": "Product documents not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(obj, context={"request": request})
        return Response(serializer.data)


class ProductListAPIView(generics.ListAPIView):
    """
    GET /api/products/  -> list of product items (GET only)
    """
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/products/<pk>/  -> single product detail (GET only)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"


class ProjectListAPIView(generics.ListAPIView):
    """
    GET /api/projects/  -> list of projects
    (ListAPIView only implements GET)
    """
    queryset = Project.objects.all().order_by("-project_date").prefetch_related("images")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]  # change to IsAuthenticated if needed


class ProjectDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/projects/<pk>/  -> single project detail
    (RetrieveAPIView only implements GET)
    """
    queryset = Project.objects.all().prefetch_related("images")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"

class EventListAPIView(generics.ListAPIView):
    """
    GET /api/events/  -> list of events (GET-only)
    """
    queryset = Event.objects.all().order_by("-event_date").prefetch_related("images")
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


class EventDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/events/<pk>/  -> event detail (GET-only)
    """
    queryset = Event.objects.all().prefetch_related("images")
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"

class JobCreateAPIView(generics.CreateAPIView):
    """
    POST /api/jobs/  -> create a Job (POST-only)
    """
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.AllowAny]

class DesignOrderCreateAPIView(generics.CreateAPIView):
    """
    POST /api/jobs/  -> create a Job (POST-only)
    """
    queryset = DesignOrder.objects.all()
    serializer_class = DesignOrderCreateSerializer
    permission_classes = [permissions.AllowAny]
