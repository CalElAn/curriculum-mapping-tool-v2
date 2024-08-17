from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, Page
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django_rulebase import Validator
from inertia.utils import InertiaJsonEncoder
from django.db.models.fields.files import ImageFieldFile
from neomodel import StructuredNode, StructuredRel
import environ, os

items_per_page = 7


class NeomodelAwareJsonEncoder(InertiaJsonEncoder):
    def default(self, value):
        if isinstance(value, StructuredNode) or isinstance(value, StructuredRel):
            return value.__properties__

        return super().default(value)


def validate(request, rules: dict[str, str]) -> dict[any, bool | list | list]:
    validator = Validator(rules)

    validation_results = validator.run_validation(request.body_json)

    if not validator.valid:
        raise ValidationError(validator.errors)

    return validation_results


def validate_unique_node_attribute(
    node: type[StructuredNode],
    attribute: str,
    attribute_value: str | int,
    exclude_attribute_value_on_node: type[StructuredNode] | None = None,
):
    all_nodes = node.nodes.all()

    if exclude_attribute_value_on_node:
        all_nodes = list(
            filter(
                lambda item: str(getattr(item, attribute)).lower()
                != str(getattr(exclude_attribute_value_on_node, attribute)).lower(),
                all_nodes,
            )
        )

    # Not using __iexact because of error when attribute is an IntegerProperty
    if list(
        filter(
            lambda item: str(getattr(item, attribute)).lower()
            == str(attribute_value).lower(),
            all_nodes,
        )
    ):
        raise ValidationError({attribute: f"must be unique"})


def redirect_back(request) -> HttpResponseRedirect:
    return redirect(request.META.get("HTTP_REFERER", "/"))


def paginate(items: list[any], page_number: int) -> tuple[Paginator, Page]:
    paginator = Paginator(items, items_per_page, allow_empty_first_page=True)

    page_obj = paginator.page(page_number)

    return paginator, page_obj


def get_page_obj_props(page_obj: Page, paginator: Paginator) -> dict[str, any]:
    return {
        "hasPrevious": page_obj.has_previous,
        "previousPageNumber": (
            page_obj.previous_page_number if page_obj.has_previous() else None
        ),
        "hasNext": page_obj.has_next,
        "nextPageNumber": (page_obj.next_page_number if page_obj.has_next() else None),
        "numPages": page_obj.paginator.num_pages,
        "currentPage": page_obj.number,
        "pageRange": list(paginator.page_range),
    }


def get_env() -> environ.Env:
    env = environ.Env()

    environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, ".env"))

    return env
