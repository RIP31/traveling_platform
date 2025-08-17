from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email Address")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Your Message")