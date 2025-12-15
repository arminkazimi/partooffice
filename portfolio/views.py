import time

# Create your views here.
from django.shortcuts import render, get_object_or_404

from .models import AboutMe, Product, Project, Event, ContactMe


def landing(request):
    # Get the first (and only) AboutMe entry
    about = AboutMe.objects.first()
    projects = Project.objects.all().order_by('-created_at')

    context = {'office': True, 'active_section': 'projects', 'projects': projects, 'object': about, }
    request.session['current_content'] = 'office'

    return render(request, 'portfolio/landing.html', context=context)


def toggle_page(request):
    current = request.session.get('current_content', 'office')
    if current == 'office':
        request.session['current_content'] = 'parto'
        # Get the first (and only) AboutMe entry
        about = AboutMe.objects.first()
        context = {'active_section': 'description', 'object': about, }
        return render(request, 'portfolio/partials/parto/index.html', context=context)
    elif current == 'parto':
        request.session['current_content'] = 'office'
        # # Get the first (and only) AboutMe entry
        # about = AboutMe.objects.first()
        projects = Project.objects.all().order_by('-created_at')

        context = {'active_section': 'projects', 'projects': projects}
        return render(request, 'portfolio/partials/office/index.html', context=context)


def description(request):
    # Get the first (and only) AboutMe entry
    about = AboutMe.objects.first()
    context = {'active_section': 'description', 'object': about, }
    return render(request, 'portfolio/partials/parto/description.html', context)


def event(request):
    context = {'active_section': 'events', }
    return render(request, 'portfolio/partials/parto/events.html', context)


def event_list_view(request):
    events = Event.objects.all().order_by('-created_at')
    context = {'active_section': 'events', 'events': events}
    return render(request, 'portfolio/partials/parto/events.html', context)


def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {'event': event, 'images': event.images.all()}
    return render(request, 'portfolio/partials/parto/event-detail.html', context)


def contact(request):
    contact_me = ContactMe.objects.first()
    context = {'active_section': 'contacts', 'object':contact_me}
    return render(request, 'portfolio/partials/parto/contacts.html', context)


def job(request):
    context = {'active_section': 'jobs', }
    return render(request, 'portfolio/partials/parto/jobs.html', context)


def project_list_view(request):
    projects = Project.objects.all().order_by('-created_at')
    context = {'active_section': 'projects', 'projects': projects}
    return render(request, 'portfolio/partials/office/projects.html', context)


def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {'project': project, 'images': project.images.all()}
    return render(request, 'portfolio/partials/office/project.html', context)


def get_product_view(request):
    product = Product.objects.first()
    # time.sleep(3)
    context = {'active_section': 'production', 'product': product, }
    return render(request, 'portfolio/partials/office/production.html', context)


def create_design_view(request):
    context = {'active_section': 'design_form', }
    return render(request, 'portfolio/partials/office/design-form.html', context)


def education_view(request):
    context = {'active_section': 'education', }
    return render(request, 'portfolio/partials/office/education.html', context)
