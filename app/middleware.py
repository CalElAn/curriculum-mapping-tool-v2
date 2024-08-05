import json
from pprint import pprint

from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from inertia import share


def inertia_share(get_response):
    def middleware(request):
        share(
            request,
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
        if (
            isinstance(exception, ValidationError)
            and request.META.get("HTTP_X_INERTIA") == "true"
        ):
            request.session["errors"] = exception.message_dict

            return redirect(request.META.get("HTTP_REFERER"))

        return None


def set_request_body_json(get_response):
    def middleware(request):
        request.body_json = (
            json.loads(request.body.decode("utf-8")) if request.body else {}
        )

        return get_response(request)

    return middleware
