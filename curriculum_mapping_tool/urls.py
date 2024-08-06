"""
URL configuration for curriculum_mapping_tool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path

from app.views.sign_up_view import SignUpView

urlpatterns = [
    path("", include("app.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    # path(
    #     "accounts/login/",
    #     LoginView.as_view(
    #         template_name="admin/login.html",
    #         extra_context={
    #             "title": "Login",
    #             "site_title": "Curriculum Mapping Tool",
    #             "site_header": "Curriculum Mapping Tool | Login",
    #         },
    #     ),
    # ),
]
