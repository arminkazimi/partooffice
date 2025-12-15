from django.urls import path

from .views import *

urlpatterns = [
    path("", landing, name='landing'),
    path("toggle/", toggle_page, name='toggle'),
    path("description/", description, name='description'),
    path("event/list/", event_list_view, name='event-list'),
    path("event/<int:pk>/", event_detail_view, name='event-detail'),
    path("contacts/", contact, name='contacts'),
    path("jobs/", job, name='jobs'),

    path("project/list/", project_list_view, name='project-list'),
    path("project/<int:pk>/", project_detail_view, name='project-detail'),
    path("product/", get_product_view, name='product-retrieve'),
    path("design/create/", create_design_view, name='design-create'),
    path("education/", education_view, name='education'),
]
