from django.http import JsonResponse
from django.views.decorators.http import (require_GET, require_POST)
from inertia import inertia

from app.cypher_queries import get_nodes_with_relationships
from app.helpers import (NeomodelAwareJsonEncoder, get_page_obj_props,
                         paginate, redirect_back, validate,
                         validate_unique_node_attribute)
from app.models import (Course, Covers, KnowledgeArea, Teaches, Topic,
                        relationship_levels)


@inertia("Topic/Form")
@require_GET
def topics_list(request):
    request_filter = request.GET.get("filter", "")

    topics = Topic.nodes.filter(title__icontains=request_filter).order_by("title").all()

    paginator, page_obj = paginate(topics, request.GET.get("page", 1))

    return {
        "initialTopics": page_obj.object_list,
        "pageObj": get_page_obj_props(page_obj, paginator),
        "allCourses": Course.nodes.order_by("number").all(),
        "allKnowledgeAreas": KnowledgeArea.nodes.order_by("title").all(),
        "levels": list(relationship_levels.values()),
        "filter": request_filter,
    }


@require_GET
def get_courses(request, topic_uid):
    return JsonResponse(
        get_nodes_with_relationships(
            Course, Teaches, Topic, Topic, topic_uid, [[Course, "number"]]
        ),
        safe=False,
        encoder=NeomodelAwareJsonEncoder,
    )


@require_GET
def get_knowledge_areas(request, topic_uid):
    return JsonResponse(
        get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea, Topic, topic_uid, [[KnowledgeArea, "title"]]
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
        },
    )

    validate_unique_node_attribute(Topic, "title", request.body_json["title"])

    topic = Topic(**{key: request.body_json[key] for key in validation_results}).save()

    request.session["data"] = {"uid": topic.uid}

    return redirect_back(request)


@require_POST
def update(request, topic_uid):
    validation_results = validate(
        request,
        {
            "title": "required",
        },
    )

    topic = Topic.nodes.get(uid=topic_uid)

    validate_unique_node_attribute(Topic, "title", request.body_json["title"], topic)

    for key in validation_results:
        setattr(topic, key, request.body_json[key])

    topic.save()

    return redirect_back(request)


@require_POST
def destroy(request, topic_uid):
    Topic.nodes.get(uid=topic_uid).delete()

    return redirect_back(request)
