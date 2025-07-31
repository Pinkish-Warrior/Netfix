from datetime import date

from django.shortcuts import render

from users.models import User, Company
from services.models import Service


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    # fetches the customer user
    user = User.objects.get(username=name)
    today = date.today()
    age = today.year - user.customer.birth_date.year - ((today.month, today.day) < (user.customer.birth_date.month, user.customer.birth_date.day))
    return render(request, 'users/profile.html', {'user': user, 'user_age': age})


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})
