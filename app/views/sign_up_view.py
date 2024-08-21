from django.contrib.auth.forms import UserCreationForm
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "registration/signup.html"