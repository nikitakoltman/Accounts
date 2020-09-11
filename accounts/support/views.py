from django.shortcuts import render


def index(request):
	return render(request, 'support.html')


def donation(request):
    return render(request, 'donation.html')


def protection(request):
    return render(request, 'protection.html')
