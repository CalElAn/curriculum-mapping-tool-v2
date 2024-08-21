from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

from app.cypher_queries import (delete_relationship,
                                get_nodes_with_relationships, get_relationship)
from app.helpers import redirect_back, validate
from app.models import Covers, KnowledgeArea, Topic


@require_POST
def store(request):
    validate(
        request,
        {
            "level": "required",
            "tools": "required",
            "comments": "required",
        },
    )

    knowledge_areas_covers_topics = get_nodes_with_relationships(
        Topic, Covers, KnowledgeArea
    )

    request_knowledge_area_uid = request.body_json["knowledge_area_uid"]
    request_topic_uid = request.body_json["topic_uid"]

    if list(
        filter(
            lambda item: getattr(item["KnowledgeArea"], "uid")
            == request_knowledge_area_uid
            and getattr(item["Topic"], "uid") == request_topic_uid,
            knowledge_areas_covers_topics,
        )
    ):
        raise ValidationError({"relationship": "must be unique"})

    covers = Topic.nodes.get(uid=request_topic_uid).covers.connect(
        KnowledgeArea.nodes.get(uid=request_knowledge_area_uid),
        {
            "level": request.body_json["level"],
            "tools": request.body_json["tools"],
            "comments": request.body_json["comments"],
        },
    )

    covers.save()

    request.session["data"] = {"uid": covers.uid}

    return redirect_back(request)


@require_POST
def update(request, covers_uid):
    validate(
        request,
        {
            "level": "required",
            "tools": "required",
            "comments": "required",
        },
    )

    covers = get_relationship(Covers, covers_uid)

    covers.level = request.body_json["level"]
    covers.tools = request.body_json["tools"]
    covers.comments = request.body_json["comments"]

    covers.save()

    return redirect_back(request)


@require_POST
def destroy(request, covers_uid):
    delete_relationship(Covers, covers_uid)

    return redirect_back(request)
