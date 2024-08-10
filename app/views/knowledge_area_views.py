import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from inertia import inertia
from django.core.paginator import Paginator
from neomodel import Q
import json
from inertia.utils import InertiaJsonEncoder
from pprint import pprint
from django_rulebase.validator import Validator
from app.cypher_queries import get_nodes_with_relationships
from app.helpers import (
    NeomodelAwareJsonEncoder,
    validate,
    redirect_back,
    paginate,
    get_page_obj_props,
    validate_unique_node_attribute,
)
from app.models import (
    Topic,
    Course,
    relationship_levels,
    Teaches,
    KnowledgeArea,
    Covers,
)


@inertia("KnowledgeArea/Form")
@require_GET
def knowledge_areas_list(request):
    request_filter = request.GET.get("filter", "")

    knowledge_areas = (
        KnowledgeArea.nodes.filter(
            Q(title__icontains=request_filter)
            | Q(description__icontains=request_filter)
        )
        .order_by("title")
        .all()
    )

    paginator, page_obj = paginate(knowledge_areas, request.GET.get("page", 1))

    return {
        "initialKnowledgeAreas": page_obj.object_list,
        "pageObj": get_page_obj_props(page_obj, paginator),
        "allTopics": Topic.nodes.order_by("name").all(),
        "levels": list(relationship_levels.values()),
        "filter": request_filter,
    }


@require_GET
def get_topics(request, knowledge_area_uid):
    return JsonResponse(
        get_nodes_with_relationships(
            Topic,
            Covers,
            KnowledgeArea,
            KnowledgeArea,
            knowledge_area_uid,
            [[Topic, "name"]],
        ),
        safe=False,
        encoder=NeomodelAwareJsonEncoder,
    )


@require_POST
def store(request):
    validation_results = validate(
        request,
        {
            "title": "required",
            "description": "required",
        },
    )

    validate_unique_node_attribute(KnowledgeArea, "title", request.body_json["title"])

    knowledge_area = KnowledgeArea(
        **{key: request.body_json[key] for key in validation_results}
    ).save()

    request.session["data"] = {"uid": knowledge_area.uid}

    return redirect_back(request)


@require_POST
def update(request, knowledge_area_uid):
    validation_results = validate(
        request,
        {
            "title": "required",
            "description": "required",
        },
    )

    knowledge_area = KnowledgeArea.nodes.get(uid=knowledge_area_uid)

    validate_unique_node_attribute(
        KnowledgeArea, "title", request.body_json["title"], knowledge_area
    )

    for key in validation_results:
        setattr(knowledge_area, key, request.body_json[key])

    knowledge_area.save()

    return redirect_back(request)


@require_POST
def destroy(request, knowledge_area_uid):
    KnowledgeArea.nodes.get(uid=knowledge_area_uid).delete()

    return redirect_back(request)
