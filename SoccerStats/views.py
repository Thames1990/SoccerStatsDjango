from django.shortcuts import render


def error403(request):
    return render(request, 'footballData/403.html')


def error404(request):
    return render(request, 'footballData/404.html')


def error500(request):
    return render(request, 'footballData/500.html')
