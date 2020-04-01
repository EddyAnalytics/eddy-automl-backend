from django.http import HttpResponse


# Create your views here.
def test_page(request):
    return HttpResponse("test page!!!!")
