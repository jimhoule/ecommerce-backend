from django.shortcuts import render
from store.models import Customer


def say_hello(request):
    query_set = Customer.objects.all()

    return render(request, 'hello.html', {'name': 'Charles', 'customers': list(query_set)})
