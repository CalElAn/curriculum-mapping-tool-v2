from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django_rulebase import Validator
from inertia.utils import InertiaJsonEncoder
from django.db.models.fields.files import ImageFieldFile
from neomodel import StructuredNode, StructuredRel


class NeomodelAwareJsonEncoder(InertiaJsonEncoder):
    def default(self, value):
        if isinstance(value, StructuredNode) or isinstance(value, StructuredRel):
            return value.__properties__

        return super().default(value)


def set_session_data(request, data: dict):
    # might not need it but just in case I need to clear session["data"] before setting it
    # since it persists during the whole session
    if "data" in request.session:
        del request.session["data"]

    request.session["data"] = data


def validate(request, rules: dict[str, str]) -> dict[any, bool | list | list]:
    validator = Validator(rules)

    validation_results = validator.run_validation(request.body_json)

    if not validator.valid:
        raise ValidationError(validator.errors)

    return validation_results


def redirect_back(request):
    return redirect(request.META.get("HTTP_REFERER"))
