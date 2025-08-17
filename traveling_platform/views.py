from .forms import ContactForm
from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def contact(request):
    form = ContactForm()
    return render(request, "contact.html", {"form": form})

def about(request):
    return render(request, "about.html")