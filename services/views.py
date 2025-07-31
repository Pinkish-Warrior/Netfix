from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    if request.method == "POST":
        form = CreateNewService(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = Company.objects.get(user=request.user)
            service.field = service.company.field
            service.save()
            return redirect('services_list')
    else:
        form = CreateNewService()
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    service = Service.objects.get(id=id)
    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = Customer.objects.get(user=request.user)
            service_request.service = service
            service_request.save()
            return redirect('services_list')
    else:
        form = RequestServiceForm()
    return render(request, 'services/request_service.html', {'form': form, 'service': service})
