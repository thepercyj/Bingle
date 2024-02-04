from django.shortcuts import render

# Index Page
def index(request):
    return render(request, 'index.html')
