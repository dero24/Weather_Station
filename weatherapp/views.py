from django.template.response import TemplateResponse
from weatherapp.models import Reading

def home(request):
    data = Reading.objects.last() # last set of weather readings we've taken with the program (most current results)
    return TemplateResponse(request, 'index.html', {'data': data})

