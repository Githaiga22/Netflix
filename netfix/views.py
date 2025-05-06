from django.shortcuts import render
from datetime import date
from users.models import User, Company, Customer
from services.models import Service, RequestService


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    user = User.objects.get(username=name)

    # Initialize as an empty list to avoid errors if user is not a customer
    requested_services = []
    today = date.today()
    dob= user.customer.birth

    user_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    # Ensure the user has a related Customer object
    requested_services = RequestService.objects.filter( user=Customer.objects.get(user=user)).order_by("-date")  # Filter by the Customer
    for service in requested_services:
        service.price = service.service.price_hour * service.hours

    return render(request, 'users/profile.html', {
        'user': user,
        'services': requested_services,
        'user_age': user_age
    })



def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")
    return render(request, 'users/profile.html', {'user': user, 'services': services})
