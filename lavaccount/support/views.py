from django.shortcuts import render
from lavaccount.settings import static_version


def support(request):
    context = {
        'static_version': static_version
    }
    return render(request, 'support/support.html', context)


def donation(request):
    context = {
        'static_version': static_version
    }
    return render(request, 'support/donation.html', context)


def protection(request):
    context = {
        'static_version': static_version
    }
    return render(request, 'support/protection.html', context)


def privacy(request):
    context = {
        'face': 'Колтманом Никитой Николаевичем',
        'protocol': 'https://',
        'domain': 'lavaccount.ru',
        'email': 'support@lavaccount.ru',
        'static_version': static_version
    }
    return render(request, 'support/privacy.html', context)


def terms(request):
    context = {
        'static_version': static_version
    }
    return render(request, 'support/terms.html', context)
