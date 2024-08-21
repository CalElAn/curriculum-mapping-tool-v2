import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import resolve
from inertia import share

from app.helpers import redirect_back


def is_inertia_request(request) -> bool:
    return (
        request.META.get("HTTP_X_INERTIA") == "true"
        or request.META.get("HTTP_X_INERTIA") == True
    )


def inertia_share(get_response):
    def middleware(request):
        share(
            request,
            auth={
                "user": request.user,
            },
            session={
                "data": request.session.get("data", None),
            },
            errors=request.session.get("errors", None),
        )

        return get_response(request)

    return middleware


class HandleInertiaValidationErrors:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "errors" in request.session:
            del request.session["errors"]

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError) and is_inertia_request(request):
            request.session["errors"] = exception.message_dict

            return redirect_back(request)

        return None


def set_request_body_json(get_response):
    def middleware(request):
        request.body_json = (
            json.loads(request.body.decode("utf-8"))
            if is_inertia_request(request) and request.body
            else {}
        )

        return get_response(request)

    return middleware


def login_required_middleware(get_response):
    def middleware(request):
        if (
            resolve(request.path_info).app_name == "app"
            and not request.user.is_authenticated
        ):
            return redirect("login")

        return get_response(request)

    return middleware


def superuser_required_middleware(get_response):
    def middleware(request):
        # url names should be in the format of e.g. "courses.list"
        protected_url_name_prefixes = ["courses", "knowledge_areas"]
        protected_url_name_suffixes = ["store", "update", "destroy"]

        request_url_name = resolve(request.path_info).url_name.split(".")

        if (
            request_url_name[0] in protected_url_name_prefixes
            and request_url_name[1] in protected_url_name_suffixes
        ):
            if request.user.is_superuser:
                return get_response(request)

            return JsonResponse(
                {
                    "message": "This action can only be performed by an admin",
                },
                status=403,
            )

        return get_response(request)

    return middleware
