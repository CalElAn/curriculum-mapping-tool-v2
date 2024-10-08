from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import (require_GET, require_POST)
from inertia import inertia
from neomodel import Q

from app.cypher_queries import get_nodes_with_relationships
from app.helpers import (NeomodelAwareJsonEncoder, get_page_obj_props,
                         paginate, redirect_back, validate,
                         validate_unique_node_attribute)
from app.models import (Covers, KnowledgeArea, Topic,
                        relationship_levels)


@inertia("KnowledgeArea/Form")
@require_GET
def knowledge_areas_list(request) -> dict[str, any]:
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
        "allTopics": Topic.nodes.order_by("title").all(),
        "levels": list(relationship_levels.values()),
        "filter": request_filter,
    }


@require_GET
def get_topics(request, knowledge_area_uid: str) -> JsonResponse:
    return JsonResponse(
        get_nodes_with_relationships(
            Topic,
            Covers,
            KnowledgeArea,
            KnowledgeArea,
            knowledge_area_uid,
            [[Topic, "title"]],
        ),
        safe=False,
        encoder=NeomodelAwareJsonEncoder,
    )


@require_POST
def store(request) -> HttpResponseRedirect:
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
def update(request, knowledge_area_uid: str) -> HttpResponseRedirect:
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
def destroy(request, knowledge_area_uid: str) -> HttpResponseRedirect:
    KnowledgeArea.nodes.get(uid=knowledge_area_uid).delete()

    return redirect_back(request)
