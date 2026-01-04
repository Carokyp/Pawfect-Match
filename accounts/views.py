from django.http import HttpResponse


def test_view(request):
    return HttpResponse("Welcome to Pawfect Match!")
