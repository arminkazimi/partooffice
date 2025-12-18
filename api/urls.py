from django.urls import path

from .views import (
    ProjectListAPIView,
    ProjectDetailAPIView,
    AboutMeAPIView,
    ContactMeAPIView,
    EducationListAPIView,
    ProductDocAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    EventListAPIView, EventDetailAPIView, JobCreateAPIView,
)

urlpatterns = [
    path("about/", AboutMeAPIView.as_view(), name="about-me"),
    path("contact/", ContactMeAPIView.as_view(), name="contact-me"),
    path("product-doc/", ProductDocAPIView.as_view(), name="product-doc"),
    path('products/', ProductListAPIView().as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path("educations/", EducationListAPIView.as_view(), name="education-list"),
    path('projects/', ProjectListAPIView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),

    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),

    path('jobs/create/', JobCreateAPIView.as_view(), name='job-create'),
    path('design/create/', JobCreateAPIView.as_view(), name='designorder-create'),
]
