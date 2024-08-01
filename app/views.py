from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_GET
from inertia import inertia


@inertia('Home')
@require_GET
def index(request):
    return {
        'events': 'pp',
    }
